# Track Usage with Idempotency using Autumn

Write a Node.js script that records a usage event with Autumn's `track` endpoint using an idempotency key to prevent duplicate billing on retries.

Implement the following at `/home/user/myproject`:

- `track_usage.js` — Generates a unique idempotency key, tracks 1 unit of `"api-calls"` for `user_test_001`, and saves the result to `track_result.json`

Use `autumn-js` SDK. The `AUTUMN_SECRET_KEY` environment variable is available. Run with `node track_usage.js`.

The script must:
1. Generate a unique `idempotencyKey` using `crypto.randomUUID()`, or use `process.env.IDEMPOTENCY_KEY` if set.
2. Call `autumn.customers.track` with:
   - `customerId`: `"user_test_001"`
   - `featureId`: `"api-calls"`
   - `value`: `1`
   - `idempotencyKey`: the generated key
3. Save the returned result to `/home/user/myproject/track_result.json`.
4. Be idempotency-safe: running twice with the same `IDEMPOTENCY_KEY` env variable must only record usage once.
