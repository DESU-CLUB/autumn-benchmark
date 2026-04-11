# Prorated Plan Upgrade with Preview using Autumn

Build an Express.js billing upgrade flow with preview and confirmation endpoints using Autumn's `billing.previewAttach` and `attach` methods.

Implement the following at `/home/user/myproject`:

- `routes/billing.js` — Three billing routes mounted under `/billing`
- Update `index.js` to mount the billing router under `/billing`

Use `autumn-js` SDK. The `AUTUMN_SECRET_KEY` environment variable is available. Server must run on port 3000.

### `POST /billing/preview-upgrade`
- Accepts `{ "customerId": string, "targetPlanId": string }`.
- Returns HTTP 400 with `{ "error": "customerId and targetPlanId are required" }` if either field is missing.
- Calls `autumn.billing.previewAttach({ customerId, productId: targetPlanId })`.
- Returns the preview response as JSON with HTTP 200.
- On Autumn error, returns HTTP 502 with `{ "error": "Billing service unavailable", "details": err.message }`.

### `POST /billing/confirm-upgrade`
- Accepts `{ "customerId": string, "targetPlanId": string, "confirmed": boolean }`.
- Returns HTTP 400 if any field is missing.
- If `confirmed` is `false`, returns HTTP 200 with `{ "status": "cancelled" }`.
- If `confirmed` is `true`, calls `autumn.attach({ customerId, productId: targetPlanId })` and returns `{ "status": "upgraded", "customerId": customerId, "planId": targetPlanId }`.
- On error, returns HTTP 502.

### `POST /billing/batch-check`
- Accepts `{ "customerIds": string[], "featureId": string }`.
- Calls `autumn.customers.check({ customerId, featureId })` for each customer **in parallel** using `Promise.all`.
- Returns `{ "results": [{ "customerId", "allowed": boolean }] }`.
