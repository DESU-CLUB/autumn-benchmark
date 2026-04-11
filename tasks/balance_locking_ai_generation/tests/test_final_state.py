import os
import json
import pytest

PROJECT_DIR = "/home/user/myproject"
AI_GENERATOR = os.path.join(PROJECT_DIR, "ai_generator.js")
RUN_SCRIPT = os.path.join(PROJECT_DIR, "run_generation.js")
RESULT_FILE = os.path.join(PROJECT_DIR, "generation_result.json")


def test_ai_generator_exists():
    assert os.path.isfile(AI_GENERATOR), (
        f"ai_generator.js not found at {AI_GENERATOR}."
    )


def test_ai_generator_exports_generate_with_budget():
    with open(AI_GENERATOR) as f:
        content = f.read()
    assert "generateWithBudget" in content, (
        "ai_generator.js must export a generateWithBudget function."
    )


def test_ai_generator_uses_balance_lock():
    with open(AI_GENERATOR) as f:
        content = f.read()
    assert "lock" in content, (
        "ai_generator.js must use the lock parameter in autumn.customers.check."
    )
    assert "enabled" in content, (
        "ai_generator.js must set lock.enabled to true."
    )
    assert "lockId" in content or "lock_id" in content, (
        "ai_generator.js must set a lockId in the lock parameter."
    )


def test_ai_generator_calls_finalize_confirm():
    with open(AI_GENERATOR) as f:
        content = f.read()
    assert "finalize" in content, (
        "ai_generator.js must call autumn.balances.finalize."
    )
    assert "confirm" in content, (
        "ai_generator.js must finalize with action: 'confirm' on success."
    )


def test_ai_generator_calls_finalize_release():
    with open(AI_GENERATOR) as f:
        content = f.read()
    assert "release" in content, (
        "ai_generator.js must finalize with action: 'release' on error."
    )


def test_ai_generator_uses_override_value():
    with open(AI_GENERATOR) as f:
        content = f.read()
    assert "overrideValue" in content or "override_value" in content, (
        "ai_generator.js must use overrideValue when confirming the lock to reflect actual token usage."
    )


def test_ai_generator_uses_ai_tokens_feature():
    with open(AI_GENERATOR) as f:
        content = f.read()
    assert "ai-tokens" in content, (
        "ai_generator.js must use featureId 'ai-tokens'."
    )


def test_run_script_exists():
    assert os.path.isfile(RUN_SCRIPT), (
        f"run_generation.js not found at {RUN_SCRIPT}."
    )


def test_generation_result_exists():
    assert os.path.isfile(RESULT_FILE), (
        f"generation_result.json not found at {RESULT_FILE}. Run 'node run_generation.js'."
    )


def test_generation_result_is_valid_json():
    with open(RESULT_FILE) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"generation_result.json is not valid JSON: {e}")


def test_generation_result_has_confirmed_true():
    with open(RESULT_FILE) as f:
        data = json.load(f)
    assert data.get("confirmed") is True, (
        f"generation_result.json must have confirmed: true, got: {data}"
    )


def test_generation_result_has_lock_id():
    with open(RESULT_FILE) as f:
        data = json.load(f)
    lock_id = data.get("lockId") or data.get("lock_id")
    assert lock_id is not None and lock_id.startswith("completion_"), (
        f"generation_result.json must have lockId starting with 'completion_', got: {lock_id}"
    )


def test_generation_result_has_tokens_used():
    with open(RESULT_FILE) as f:
        data = json.load(f)
    tokens_used = data.get("tokensUsed") or data.get("tokens_used")
    assert isinstance(tokens_used, int) and tokens_used > 0, (
        f"generation_result.json must have tokensUsed as a positive integer, got: {tokens_used}"
    )
