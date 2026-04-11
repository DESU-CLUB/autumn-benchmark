import os
import shutil
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/myproject"


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_index_js_exists():
    index = os.path.join(PROJECT_DIR, "index.js")
    assert os.path.isfile(index), f"index.js not found at {index}."


def test_package_json_exists():
    pkg = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg), f"package.json not found at {pkg}."


def test_autumn_js_installed():
    node_modules = os.path.join(PROJECT_DIR, "node_modules", "autumn-js")
    assert os.path.isdir(node_modules), (
        f"autumn-js not found in node_modules at {node_modules}."
    )


def test_express_installed():
    node_modules = os.path.join(PROJECT_DIR, "node_modules", "express")
    assert os.path.isdir(node_modules), (
        f"express not found in node_modules at {node_modules}."
    )


def test_health_route_exists():
    index = os.path.join(PROJECT_DIR, "index.js")
    with open(index) as f:
        content = f.read()
    assert "/health" in content, (
        "index.js must contain a GET /health route returning {\"status\": \"ok\"}."
    )


def test_autumn_secret_key_env_set():
    key = os.environ.get("AUTUMN_SECRET_KEY", "")
    assert key != "", "AUTUMN_SECRET_KEY environment variable is not set."
