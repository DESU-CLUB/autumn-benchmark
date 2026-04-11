import os
import json
import pytest

PROJECT_DIR = "/home/user/myproject"
ONBOARD_SCRIPT = os.path.join(PROJECT_DIR, "onboard_customer.js")
RESULT_FILE = os.path.join(PROJECT_DIR, "onboard_result.json")


def test_onboard_script_exists():
    assert os.path.isfile(ONBOARD_SCRIPT), (
        f"onboard_customer.js not found at {ONBOARD_SCRIPT}."
    )


def test_script_uses_promise_all():
    with open(ONBOARD_SCRIPT) as f:
        content = f.read()
    assert "Promise.all" in content, (
        "onboard_customer.js must use Promise.all for parallel operations."
    )


def test_script_creates_both_customers():
    with open(ONBOARD_SCRIPT) as f:
        content = f.read()
    assert "user_test_001" in content, (
        "onboard_customer.js must create/sync customer 'user_test_001'."
    )
    assert "user_test_002" in content, (
        "onboard_customer.js must create/sync customer 'user_test_002'."
    )
    assert "getOrCreate" in content, (
        "onboard_customer.js must call autumn.customers.getOrCreate."
    )


def test_script_attaches_free_plan():
    with open(ONBOARD_SCRIPT) as f:
        content = f.read()
    assert "autumn.attach" in content or ".attach(" in content, (
        "onboard_customer.js must call autumn.attach to attach a plan."
    )
    assert "'free'" in content or '"free"' in content, (
        "onboard_customer.js must attach the 'free' product/plan."
    )


def test_result_file_exists():
    assert os.path.isfile(RESULT_FILE), (
        f"onboard_result.json not found at {RESULT_FILE}. Run 'node onboard_customer.js'."
    )


def test_result_is_valid_json():
    with open(RESULT_FILE) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"onboard_result.json is not valid JSON: {e}")


def test_result_has_customers_array():
    with open(RESULT_FILE) as f:
        data = json.load(f)
    assert "customers" in data, (
        f"onboard_result.json must have a 'customers' array, got: {data}"
    )
    assert isinstance(data["customers"], list), (
        "'customers' must be an array."
    )
    assert len(data["customers"]) == 2, (
        f"'customers' array must have 2 entries, got: {len(data['customers'])}"
    )


def test_result_customers_have_plan_attached():
    with open(RESULT_FILE) as f:
        data = json.load(f)
    for customer in data["customers"]:
        assert customer.get("planAttached") is True, (
            f"Each customer must have planAttached: true, got: {customer}"
        )


def test_result_customers_have_correct_ids():
    with open(RESULT_FILE) as f:
        data = json.load(f)
    ids = {c.get("customerId") for c in data["customers"]}
    assert "user_test_001" in ids, (
        f"onboard_result.json must include customer 'user_test_001', got: {ids}"
    )
    assert "user_test_002" in ids, (
        f"onboard_result.json must include customer 'user_test_002', got: {ids}"
    )
