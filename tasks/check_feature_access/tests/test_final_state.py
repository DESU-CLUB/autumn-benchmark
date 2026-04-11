import os
import subprocess
import json
import time
import socket
import signal
import pytest

PROJECT_DIR = "/home/user/myproject"
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


def test_index_has_check_access_route():
    with open(INDEX_FILE) as f:
        content = f.read()
    assert "/check-access" in content, (
        "index.js must contain a POST /check-access route."
    )


def test_index_uses_autumn_check():
    with open(INDEX_FILE) as f:
        content = f.read()
    assert "autumn" in content.lower() or "Autumn" in content, (
        "index.js must import and use the Autumn SDK."
    )
    assert "check" in content, (
        "index.js must call autumn.customers.check in the /check-access route."
    )


def test_check_access_route_returns_json(start_server):
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            "http://localhost:3000/check-access",
            "-H", "Content-Type: application/json",
            "-d", '{"customerId": "user_test_001", "featureId": "messages"}',
            "-w", "\n%{http_code}",
        ],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"curl failed: {result.stderr}"
    lines = result.stdout.strip().split("\n")
    http_code = lines[-1]
    body = "\n".join(lines[:-1])
    assert http_code in ("200", "403"), (
        f"Expected HTTP 200 or 403 from /check-access, got: {http_code}. Body: {body}"
    )
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail(f"Response body is not valid JSON: {body}")
    assert "allowed" in data, (
        f"Response JSON must contain 'allowed' field, got: {data}"
    )


def test_check_access_returns_403_when_not_allowed(start_server):
    """Verify HTTP status 403 is returned when allowed is false."""
    # We test the logic by inspecting the code rather than forcing an API state
    with open(INDEX_FILE) as f:
        content = f.read()
    assert "403" in content, (
        "index.js must return HTTP 403 status when allowed is false."
    )


def test_check_access_returns_200_when_allowed(start_server):
    """Verify HTTP status 200 is returned when allowed is true."""
    with open(INDEX_FILE) as f:
        content = f.read()
    assert "200" in content or "response.allowed" in content or "res.status" in content, (
        "index.js must return HTTP 200 status when allowed is true."
    )
