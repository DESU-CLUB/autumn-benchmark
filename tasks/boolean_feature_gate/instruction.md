# Boolean Feature Gate for Premium Dashboard using Autumn

Build an Express.js middleware and route that gates access to a premium dashboard using Autumn's boolean feature check.

Implement the following at `/home/user/myproject`:

- `middleware/auth.js` — Exports `requirePremium` middleware
- `routes/dashboard.js` — Protected `GET /dashboard/premium` route
- Update `index.js` to mount the dashboard router under `/dashboard`

Use `autumn-js` SDK. The `AUTUMN_SECRET_KEY` environment variable is available. Server must run on port 3000.

`requirePremium` middleware must:
- Read `x-customer-id` from request headers; return HTTP 400 with `{ "error": "Missing customer ID" }` if absent.
- Call `autumn.customers.check({ customerId, featureId: 'premium-dashboard' })`.
- Call `next()` if `allowed` is `true`.
- Return HTTP 403 with `{ "error": "Premium plan required" }` if `allowed` is `false`.

`GET /dashboard/premium` must:
- Use the `requirePremium` middleware.
- Return `{ "data": "Premium dashboard content", "customerId": "<customerId>" }` on success.
