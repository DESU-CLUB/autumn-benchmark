import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_FILE = os.path.join(PROJECT_DIR, "track_usage.js")
RESULT_FILE = os.path.join(PROJECT_DIR, "track_result.json")


def test_script_file_exists():
    assert os.path.isfile(SCRIPT_FILE), (
        f"track_usage.js not found at {SCRIPT_FILE}."
    )


def test_script_imports_autumn():
    with open(SCRIPT_FILE) as f:
        content = f.read()
    assert "autumn-js" in content or "Autumn" in content, (
        "track_usage.js must import Autumn from autumn-js."
    )


def test_script_calls_track():
    with open(SCRIPT_FILE) as f:
        content = f.read()
    assert ".track(" in content or "customers.track" in content, (
        "track_usage.js must call autumn.customers.track."
    )


def test_script_uses_correct_customer_and_feature():
    with open(SCRIPT_FILE) as f:
        content = f.read()
    assert "user_test_001" in content, (
        "track_usage.js must use customerId 'user_test_001'."
    )
    assert "api-calls" in content, (
        "track_usage.js must use featureId 'api-calls'."
    )


def test_script_uses_idempotency_key():
    with open(SCRIPT_FILE) as f:
        content = f.read()
    assert "idempotencyKey" in content or "idempotency_key" in content, (
        "track_usage.js must include an idempotencyKey to prevent duplicate usage records."
    )


def test_result_file_exists():
    assert os.path.isfile(RESULT_FILE), (
        f"track_result.json not found at {RESULT_FILE}. "
        "Run the script to generate the output file."
    )


def test_result_is_valid_json():
    with open(RESULT_FILE) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"track_result.json is not valid JSON: {e}")


def test_result_contains_value_field():
    with open(RESULT_FILE) as f:
        data = json.load(f)
    assert "value" in data, (
        f"track_result.json must contain a 'value' field from the Autumn track response. Got: {data}"
    )
