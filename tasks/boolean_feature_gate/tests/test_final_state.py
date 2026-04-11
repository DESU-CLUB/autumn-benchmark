import os
import json
import subprocess
import time
import socket
import signal
import pytest

PROJECT_DIR = "/home/user/myproject"
AUTH_MIDDLEWARE = os.path.join(PROJECT_DIR, "middleware", "auth.js")
DASHBOARD_ROUTE = os.path.join(PROJECT_DIR, "routes", "dashboard.js")
INDEX_FILE = os.path.join(PROJECT_DIR, "index.js")


def wait_for_port(port, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) == 0:
                return True
        time.sleep(1)
    return False


@pytest.fixture(scope="module")
def start_server():
    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
    )
    if not wait_for_port(3000):
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Express server failed to start on port 3000.")
    yield
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)


def test_auth_middleware_exists():
    assert os.path.isfile(AUTH_MIDDLEWARE), (
        f"middleware/auth.js not found at {AUTH_MIDDLEWARE}."
    )


def test_auth_middleware_has_require_premium():
    with open(AUTH_MIDDLEWARE) as f:
        content = f.read()
    assert "requirePremium" in content, (
        "middleware/auth.js must export a requirePremium function."
    )


def test_auth_middleware_checks_premium_dashboard():
    with open(AUTH_MIDDLEWARE) as f:
        content = f.read()
    assert "premium-dashboard" in content, (
        "middleware/auth.js must check featureId 'premium-dashboard'."
    )
    assert "autumn" in content.lower() or "Autumn" in content, (
        "middleware/auth.js must use the Autumn SDK."
    )


def test_auth_middleware_checks_header():
    with open(AUTH_MIDDLEWARE) as f:
        content = f.read()
    assert "x-customer-id" in content, (
        "middleware/auth.js must read the 'x-customer-id' header."
    )


def test_dashboard_route_exists():
    assert os.path.isfile(DASHBOARD_ROUTE), (
        f"routes/dashboard.js not found at {DASHBOARD_ROUTE}."
    )


def test_index_mounts_dashboard_router():
    with open(INDEX_FILE) as f:
        content = f.read()
    assert "/dashboard" in content, (
        "index.js must mount the dashboard router under '/dashboard'."
    )


def test_missing_header_returns_400(start_server):
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "http://localhost:3000/dashboard/premium"],
        capture_output=True, text=True,
    )
    assert result.stdout.strip() == "400", (
        f"GET /dashboard/premium without x-customer-id must return HTTP 400, got: {result.stdout.strip()}"
    )


def test_with_customer_id_returns_200_or_403(start_server):
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "-H", "x-customer-id: user_test_001",
         "http://localhost:3000/dashboard/premium"],
        capture_output=True, text=True,
    )
    code = result.stdout.strip()
    assert code in ("200", "403"), (
        f"GET /dashboard/premium with x-customer-id must return 200 or 403, got: {code}"
    )
