# AI Generation with Balance Locking using Autumn

Build a Node.js module that simulates an AI completion flow using Autumn's balance locking pattern to safely reserve and confirm token usage.

Implement the following at `/home/user/myproject`:

- `ai_generator.js` — Exports `generateWithBudget(customerId, maxTokens)` implementing the lock → work → finalize pattern
- `run_generation.js` — Calls `generateWithBudget('user_test_001', 1000)` and writes the result to `generation_result.json`

Use `autumn-js` SDK. The `AUTUMN_SECRET_KEY` environment variable is available. Run with `node run_generation.js`.

`generateWithBudget(customerId, maxTokens)` must:
1. Generate a unique `lockId` like `completion_<uuid>`.
2. Call `autumn.customers.check` with `featureId: 'ai-tokens'`, `requiredBalance: maxTokens`, `sendEvent: true`, and `lock: { enabled: true, lockId, expiresAt: Date.now() + 60000 }`.
3. If `allowed` is `false`, throw `Error('Insufficient ai-tokens balance')`.
4. Simulate AI work (100ms delay) returning `tokensUsed = Math.floor(maxTokens * 0.75)`.
5. Call `autumn.balances.finalize({ lockId, action: 'confirm', overrideValue: tokensUsed })`.
6. Return `{ lockId, tokensUsed, confirmed: true }`.
7. On error during the work phase, call `autumn.balances.finalize({ lockId, action: 'release' })` and re-throw.
