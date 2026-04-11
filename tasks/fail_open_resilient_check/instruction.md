# Fail-Open Resilient Feature Check with Autumn

Build a Node.js utility module that wraps Autumn's feature check with a fail-open pattern to keep your app available when the Autumn API is unreachable.

Implement the following at `/home/user/myproject`:

- `resilient_check.js` — Exports `resilientCheck` and `resilientCheckStrict` functions
- `demo_check.js` — Runs `resilientCheck('user_test_001', 'messages')` and writes the result to `check_result.json`

Use `autumn-js` SDK. The `AUTUMN_SECRET_KEY` environment variable is available. Run with `node demo_check.js`.

`resilientCheck(customerId, featureId)` must:
- Call `autumn.customers.check({ customerId, featureId })`.
- Return `{ allowed: true, source: 'autumn' }` on success.
- On any error (network, timeout, 5xx), log `"AUTUMN UNREACHABLE, FAILING OPEN"` to stderr and return `{ allowed: true, source: 'fail-open' }`.

`resilientCheckStrict(customerId, featureId)` must:
- Use a separate Autumn instance configured with `failOpen: false`.
- Re-throw any errors (does not fail open).
- Return `{ allowed: result.allowed, source: 'autumn-strict' }` on success.
