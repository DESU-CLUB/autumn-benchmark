import os
import json
import pytest

PROJECT_DIR = "/home/user/myproject"
RESILIENT_CHECK = os.path.join(PROJECT_DIR, "resilient_check.js")
DEMO_SCRIPT = os.path.join(PROJECT_DIR, "demo_check.js")
RESULT_FILE = os.path.join(PROJECT_DIR, "check_result.json")


def test_resilient_check_exists():
    assert os.path.isfile(RESILIENT_CHECK), (
        f"resilient_check.js not found at {RESILIENT_CHECK}."
    )


def test_resilient_check_exports_resilient_check():
    with open(RESILIENT_CHECK) as f:
        content = f.read()
    assert "resilientCheck" in content, (
        "resilient_check.js must export a resilientCheck function."
    )


def test_resilient_check_has_try_catch():
    with open(RESILIENT_CHECK) as f:
        content = f.read()
    assert "try" in content and "catch" in content, (
        "resilientCheck must wrap the Autumn call in a try-catch block for fail-open behavior."
    )


def test_resilient_check_returns_fail_open_on_error():
    with open(RESILIENT_CHECK) as f:
        content = f.read()
    assert "fail-open" in content, (
        "resilientCheck must return source: 'fail-open' when Autumn is unreachable."
    )


def test_resilient_check_exports_strict_check():
    with open(RESILIENT_CHECK) as f:
        content = f.read()
    assert "resilientCheckStrict" in content, (
        "resilient_check.js must export a resilientCheckStrict function."
    )


def test_strict_check_uses_fail_open_false():
    with open(RESILIENT_CHECK) as f:
        content = f.read()
    assert "failOpen" in content or "fail_open" in content, (
        "resilientCheckStrict must use failOpen: false in the Autumn constructor."
    )


def test_demo_script_exists():
    assert os.path.isfile(DEMO_SCRIPT), (
        f"demo_check.js not found at {DEMO_SCRIPT}."
    )


def test_check_result_exists():
    assert os.path.isfile(RESULT_FILE), (
        f"check_result.json not found at {RESULT_FILE}. Run 'node demo_check.js'."
    )


def test_check_result_is_valid_json():
    with open(RESULT_FILE) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"check_result.json is not valid JSON: {e}")


def test_check_result_has_allowed_field():
    with open(RESULT_FILE) as f:
        data = json.load(f)
    assert "allowed" in data, (
        f"check_result.json must contain an 'allowed' field, got: {data}"
    )
    assert isinstance(data["allowed"], bool), (
        f"'allowed' field must be a boolean, got: {type(data['allowed'])}"
    )


def test_check_result_has_source_field():
    with open(RESULT_FILE) as f:
        data = json.load(f)
    source = data.get("source")
    assert source in ("autumn", "fail-open"), (
        f"check_result.json 'source' must be 'autumn' or 'fail-open', got: {source}"
    )
