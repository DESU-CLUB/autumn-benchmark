import os
import shutil
import json
import pytest

PROJECT_DIR = "/home/user/myproject"


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_package_json_exists():
    assert os.path.isfile(os.path.join(PROJECT_DIR, "package.json")), (
        "package.json not found in project directory."
    )


def test_autumn_js_installed():
    assert os.path.isdir(os.path.join(PROJECT_DIR, "node_modules", "autumn-js")), (
        "autumn-js not found in node_modules."
    )


def test_package_json_type_module():
    with open(os.path.join(PROJECT_DIR, "package.json")) as f:
        data = json.load(f)
    assert data.get("type") == "module", "package.json must have \"type\": \"module\"."


def test_autumn_secret_key_env_set():
    assert os.environ.get("AUTUMN_SECRET_KEY", "") != "", (
        "AUTUMN_SECRET_KEY environment variable is not set."
    )
