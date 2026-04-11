import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_FILE = os.path.join(PROJECT_DIR, "create_customer.js")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "output.json")


def test_script_file_exists():
    assert os.path.isfile(SCRIPT_FILE), (
        f"create_customer.js not found at {SCRIPT_FILE}. "
        "The script must be created to call autumn.customers.getOrCreate."
    )


def test_script_uses_autumn_sdk():
    with open(SCRIPT_FILE) as f:
        content = f.read()
    assert "autumn-js" in content or "Autumn" in content, (
        "create_customer.js must import and use the Autumn SDK from autumn-js."
    )
    assert "getOrCreate" in content, (
        "create_customer.js must call customers.getOrCreate."
    )


def test_script_uses_correct_customer_id():
    with open(SCRIPT_FILE) as f:
        content = f.read()
    assert "user_test_001" in content, (
        "create_customer.js must use customerId 'user_test_001'."
    )


def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), (
        f"output.json not found at {OUTPUT_FILE}. "
        "Run the script and redirect stdout to output.json."
    )


def test_output_is_valid_json():
    with open(OUTPUT_FILE) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"output.json is not valid JSON: {e}")


def test_output_contains_customer_id():
    with open(OUTPUT_FILE) as f:
        data = json.load(f)
    # SDK may return camelCase or snake_case depending on version
    customer_id = data.get("customerId") or data.get("customer_id") or data.get("id")
    assert customer_id == "user_test_001", (
        f"Expected customerId 'user_test_001' in output.json, got: {customer_id}. "
        f"Full response: {data}"
    )


def test_output_contains_name():
    with open(OUTPUT_FILE) as f:
        data = json.load(f)
    name = data.get("name")
    assert name == "Alice Testuser", (
        f"Expected name 'Alice Testuser' in output.json, got: {name}."
    )


def test_output_contains_email():
    with open(OUTPUT_FILE) as f:
        data = json.load(f)
    email = data.get("email")
    assert email == "alice@example.com", (
        f"Expected email 'alice@example.com' in output.json, got: {email}."
    )
