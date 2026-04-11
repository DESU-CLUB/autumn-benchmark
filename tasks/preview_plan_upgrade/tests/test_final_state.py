import os
import json
import subprocess
import time
import socket
import signal
import pytest

PROJECT_DIR = "/home/user/myproject"
BILLING_ROUTE = os.path.join(PROJECT_DIR, "routes", "billing.js")
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


def test_billing_route_file_exists():
    assert os.path.isfile(BILLING_ROUTE), (
        f"routes/billing.js not found at {BILLING_ROUTE}."
    )


def test_billing_route_has_preview_upgrade():
    with open(BILLING_ROUTE) as f:
        content = f.read()
    assert "preview-upgrade" in content, (
        "routes/billing.js must have POST /preview-upgrade route."
    )


def test_billing_route_has_confirm_upgrade():
    with open(BILLING_ROUTE) as f:
        content = f.read()
    assert "confirm-upgrade" in content, (
        "routes/billing.js must have POST /confirm-upgrade route."
    )


def test_billing_route_has_batch_check():
    with open(BILLING_ROUTE) as f:
        content = f.read()
    assert "batch-check" in content, (
        "routes/billing.js must have POST /batch-check route."
    )


def test_billing_route_uses_preview_attach():
    with open(BILLING_ROUTE) as f:
        content = f.read()
    assert "previewAttach" in content or "preview_attach" in content, (
        "routes/billing.js must call autumn.billing.previewAttach for the preview-upgrade route."
    )


def test_billing_route_uses_promise_all():
    with open(BILLING_ROUTE) as f:
        content = f.read()
    assert "Promise.all" in content, (
        "routes/billing.js must use Promise.all in batch-check for parallel checks."
    )


def test_index_mounts_billing_router():
    with open(INDEX_FILE) as f:
        content = f.read()
    assert "/billing" in content, (
        "index.js must mount the billing router under '/billing'."
    )


def test_preview_upgrade_missing_body_returns_400(start_server):
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "-X", "POST", "http://localhost:3000/billing/preview-upgrade",
         "-H", "Content-Type: application/json",
         "-d", "{}"],
        capture_output=True, text=True,
    )
    assert result.stdout.strip() == "400", (
        f"POST /billing/preview-upgrade with empty body must return HTTP 400, got: {result.stdout.strip()}"
    )


def test_preview_upgrade_returns_200_or_502(start_server):
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "-X", "POST", "http://localhost:3000/billing/preview-upgrade",
         "-H", "Content-Type: application/json",
         "-d", '{"customerId": "user_test_001", "targetPlanId": "pro"}'],
        capture_output=True, text=True,
    )
    code = result.stdout.strip()
    assert code in ("200", "502"), (
        f"POST /billing/preview-upgrade must return 200 or 502, got: {code}"
    )


def test_confirm_upgrade_cancelled_returns_200(start_server):
    result = subprocess.run(
        ["curl", "-s", "-w", "\n%{http_code}",
         "-X", "POST", "http://localhost:3000/billing/confirm-upgrade",
         "-H", "Content-Type: application/json",
         "-d", '{"customerId": "user_test_001", "targetPlanId": "pro", "confirmed": false}'],
        capture_output=True, text=True,
    )
    lines = result.stdout.strip().split("\n")
    code = lines[-1]
    body = "\n".join(lines[:-1])
    assert code == "200", (
        f"POST /billing/confirm-upgrade with confirmed:false must return HTTP 200, got: {code}"
    )
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {body}")
    assert data.get("status") == "cancelled", (
        f"Expected status: 'cancelled', got: {data}"
    )


def test_batch_check_returns_results_array(start_server):
    result = subprocess.run(
        ["curl", "-s", "-w", "\n%{http_code}",
         "-X", "POST", "http://localhost:3000/billing/batch-check",
         "-H", "Content-Type: application/json",
         "-d", '{"customerIds": ["user_test_001", "user_test_002"], "featureId": "messages"}'],
        capture_output=True, text=True,
    )
    lines = result.stdout.strip().split("\n")
    code = lines[-1]
    body = "\n".join(lines[:-1])
    assert code == "200", (
        f"POST /billing/batch-check must return HTTP 200, got: {code}. Body: {body}"
    )
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail(f"batch-check response is not valid JSON: {body}")
    assert "results" in data, (
        f"batch-check response must contain 'results' array, got: {data}"
    )
    assert len(data["results"]) == 2, (
        f"batch-check results must have 2 entries, got: {len(data['results'])}"
    )
