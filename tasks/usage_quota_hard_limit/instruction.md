# Usage-Based Metering with Hard Quota Limit using Autumn

Build an Express.js API metering middleware and route that enforces a hard usage quota using Autumn's `check` and `track` endpoints.

Implement the following at `/home/user/myproject`:

- `middleware/rateLimit.js` — Exports `checkApiQuota` middleware
- `routes/api.js` — `POST /api/process` route protected by the quota middleware
- Update `index.js` to mount the API router under `/api`

Use `autumn-js` SDK. The `AUTUMN_SECRET_KEY` environment variable is available. Server must run on port 3000.

`checkApiQuota` middleware must:
- Read `x-customer-id` from request headers; return HTTP 400 with `{ "error": "Missing customer ID" }` if absent.
- Call `autumn.customers.check({ customerId, featureId: 'api-requests' })`.
- If `allowed` is `false`, return HTTP 429 with `{ "error": "API quota exceeded", "allowed": false }`.
- If `allowed` is `true`, call `autumn.customers.track({ customerId, featureId: 'api-requests', value: 1 })` then call `next()`.

`POST /api/process` must:
- Use the `checkApiQuota` middleware.
- Accept a JSON body with a `payload` field.
- Return `{ "result": "processed", "payload": "<value>", "customerId": "<id>" }`.
