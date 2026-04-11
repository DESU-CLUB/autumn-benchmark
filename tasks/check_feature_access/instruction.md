# Check Feature Access with Autumn

Add a feature access check endpoint to an existing Express.js API using Autumn's `check` endpoint.

Implement the following at `/home/user/myproject`:

- Add route `POST /check-access` to the existing `index.js`

Use `autumn-js` SDK. The `AUTUMN_SECRET_KEY` environment variable is available. Server must run on port 3000.

`POST /check-access` must:
1. Accept a JSON body with `customerId` and `featureId`.
2. Call `autumn.customers.check({ customerId, featureId })`.
3. Respond with HTTP 200 and the full Autumn response as JSON if `allowed` is `true`.
4. Respond with HTTP 403 and the full Autumn response as JSON if `allowed` is `false`.
