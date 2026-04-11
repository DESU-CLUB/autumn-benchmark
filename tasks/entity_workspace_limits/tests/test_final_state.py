import os
import json
import subprocess
import time
import socket
import signal
import pytest

PROJECT_DIR = "/home/user/myproject"
LIB_AUTUMN = os.path.join(PROJECT_DIR, "lib", "autumn.js")
WORKSPACES_ROUTE = os.path.join(PROJECT_DIR, "routes", "workspaces.js")
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


def test_lib_autumn_exists():
    assert os.path.isfile(LIB_AUTUMN), (
        f"lib/autumn.js not found at {LIB_AUTUMN}. Create it to export the Autumn SDK instance."
    )


def test_lib_autumn_initializes_sdk():
    with open(LIB_AUTUMN) as f:
        content = f.read()
    assert "Autumn" in content, (
        "lib/autumn.js must import and initialize the Autumn SDK."
    )
    assert "AUTUMN_SECRET_KEY" in content or "secretKey" in content, (
        "lib/autumn.js must use AUTUMN_SECRET_KEY for initialization."
    )


def test_workspaces_route_exists():
    assert os.path.isfile(WORKSPACES_ROUTE), (
        f"routes/workspaces.js not found at {WORKSPACES_ROUTE}."
    )


def test_workspaces_route_has_create():
    with open(WORKSPACES_ROUTE) as f:
        content = f.read()
    assert "entities.create" in content or "entities.create" in content, (
        "routes/workspaces.js must call autumn.entities.create for workspace creation."
    )


def test_workspaces_route_has_check_with_entity_id():
    with open(WORKSPACES_ROUTE) as f:
        content = f.read()
    assert "entityId" in content or "entity_id" in content, (
        "routes/workspaces.js must pass entityId to autumn.customers.check and track."
    )


def test_workspaces_route_has_track():
    with open(WORKSPACES_ROUTE) as f:
        content = f.read()
    assert ".track(" in content or "customers.track" in content, (
        "routes/workspaces.js must call autumn.customers.track for credit consumption."
    )


def test_workspaces_route_has_delete():
    with open(WORKSPACES_ROUTE) as f:
        content = f.read()
    assert "entities.delete" in content, (
        "routes/workspaces.js must call autumn.entities.delete for workspace deletion."
    )


def test_workspaces_route_has_get_balance():
    with open(WORKSPACES_ROUTE) as f:
        content = f.read()
    assert "entities.get" in content, (
        "routes/workspaces.js must call autumn.entities.get for balance retrieval."
    )


def test_index_mounts_workspaces_router():
    with open(INDEX_FILE) as f:
        content = f.read()
    assert "/workspaces" in content, (
        "index.js must mount the workspaces router under '/workspaces'."
    )


def test_create_workspace_returns_created(start_server):
    result = subprocess.run(
        ["curl", "-s", "-w", "\n%{http_code}",
         "-X", "POST", "http://localhost:3000/workspaces",
         "-H", "Content-Type: application/json",
         "-d", '{"orgId": "org_001", "workspaceId": "ws_001", "workspaceName": "Engineering"}'],
        capture_output=True, text=True,
    )
    lines = result.stdout.strip().split("\n")
    code = lines[-1]
    body = "\n".join(lines[:-1])
    assert code in ("200", "201", "502"), (
        f"POST /workspaces must return 200, 201, or 502, got: {code}. Body: {body}"
    )
    if code in ("200", "201"):
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            pytest.fail(f"Response is not valid JSON: {body}")
        assert data.get("created") is True or data.get("workspaceId") is not None, (
            f"Response must indicate workspace was created, got: {data}"
        )


def test_use_credits_returns_200_or_402(start_server):
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "-X", "POST", "http://localhost:3000/workspaces/ws_001/use-credits",
         "-H", "Content-Type: application/json",
         "-d", '{"orgId": "org_001", "amount": 5}'],
        capture_output=True, text=True,
    )
    code = result.stdout.strip()
    assert code in ("200", "402", "502"), (
        f"POST /workspaces/ws_001/use-credits must return 200, 402, or 502, got: {code}"
    )


def test_delete_workspace_returns_deleted(start_server):
    result = subprocess.run(
        ["curl", "-s", "-w", "\n%{http_code}",
         "-X", "DELETE", "http://localhost:3000/workspaces/ws_001",
         "-H", "Content-Type: application/json",
         "-d", '{"orgId": "org_001"}'],
        capture_output=True, text=True,
    )
    lines = result.stdout.strip().split("\n")
    code = lines[-1]
    body = "\n".join(lines[:-1])
    assert code in ("200", "404", "502"), (
        f"DELETE /workspaces/ws_001 must return 200, 404, or 502, got: {code}. Body: {body}"
    )
    if code == "200":
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            pytest.fail(f"Response is not valid JSON: {body}")
        assert data.get("deleted") is True, (
            f"DELETE response must have deleted: true, got: {data}"
        )
