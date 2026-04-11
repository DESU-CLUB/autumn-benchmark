import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_package_json_exists():
    pkg = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg), f"package.json not found at {pkg}."


def test_autumn_js_installed():
    node_modules = os.path.join(PROJECT_DIR, "node_modules", "autumn-js")
    assert os.path.isdir(node_modules), (
        f"autumn-js package not found in node_modules at {node_modules}. "
        "Run 'npm install autumn-js' in the project directory."
    )


def test_package_json_has_module_type():
    import json
    pkg = os.path.join(PROJECT_DIR, "package.json")
    with open(pkg) as f:
        data = json.load(f)
    assert data.get("type") == "module", (
        "package.json must have \"type\": \"module\" for ES module syntax support."
    )


def test_autumn_secret_key_env_set():
    key = os.environ.get("AUTUMN_SECRET_KEY", "")
    assert key != "", (
        "AUTUMN_SECRET_KEY environment variable is not set. "
        "It must be set before running the script."
    )
