import os
import json
import subprocess
import time
import socket
import signal
import pytest

PROJECT_DIR = "/home/user/myproject"
RATE_LIMIT_MIDDLEWARE = os.path.join(PROJECT_DIR, "middleware", "rateLimit.js")
API_ROUTE = os.path.join(PROJECT_DIR, "routes", "api.js")
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


def test_rate_limit_middleware_exists():
    assert os.path.isfile(RATE_LIMIT_MIDDLEWARE), (
        f"middleware/rateLimit.js not found at {RATE_LIMIT_MIDDLEWARE}."
    )


def test_middleware_has_check_api_quota():
    with open(RATE_LIMIT_MIDDLEWARE) as f:
        content = f.read()
    assert "checkApiQuota" in content, (
        "middleware/rateLimit.js must export checkApiQuota function."
    )


def test_middleware_calls_check_and_track():
    with open(RATE_LIMIT_MIDDLEWARE) as f:
        content = f.read()
    assert "api-requests" in content, (
        "middleware/rateLimit.js must use featureId 'api-requests'."
    )
    assert ".check(" in content or "customers.check" in content, (
        "middleware/rateLimit.js must call autumn.customers.check."
    )
    assert ".track(" in content or "customers.track" in content, (
        "middleware/rateLimit.js must call autumn.customers.track."
    )


def test_middleware_returns_429_on_quota_exceeded():
    with open(RATE_LIMIT_MIDDLEWARE) as f:
        content = f.read()
    assert "429" in content, (
        "middleware/rateLimit.js must return HTTP 429 when quota is exceeded."
    )


def test_api_route_exists():
    assert os.path.isfile(API_ROUTE), (
        f"routes/api.js not found at {API_ROUTE}."
    )


def test_index_mounts_api_router():
    with open(INDEX_FILE) as f:
        content = f.read()
    assert "/api" in content, (
        "index.js must mount the api router under '/api'."
    )


def test_missing_header_returns_400(start_server):
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "-X", "POST", "http://localhost:3000/api/process",
         "-H", "Content-Type: application/json",
         "-d", '{"payload": "test"}'],
        capture_output=True, text=True,
    )
    assert result.stdout.strip() == "400", (
        f"POST /api/process without x-customer-id must return HTTP 400, got: {result.stdout.strip()}"
    )


def test_with_customer_id_returns_200_or_429(start_server):
    result = subprocess.run(
        ["curl", "-s", "-w", "\n%{http_code}",
         "-X", "POST", "http://localhost:3000/api/process",
         "-H", "Content-Type: application/json",
         "-H", "x-customer-id: user_test_001",
         "-d", '{"payload": "hello"}'],
        capture_output=True, text=True,
    )
    lines = result.stdout.strip().split("\n")
    code = lines[-1]
    assert code in ("200", "429"), (
        f"POST /api/process with x-customer-id must return 200 or 429, got: {code}"
    )
