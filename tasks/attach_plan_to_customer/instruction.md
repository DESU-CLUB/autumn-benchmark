# Attach a Plan to a Customer with Autumn

Build a Node.js billing onboarding script that creates customers and attaches a free plan to them using Autumn's `attach` endpoint.

Implement the following at `/home/user/myproject`:

- `onboard_customer.js` — Creates two customers in parallel and attaches the `"free"` plan to both, then writes the result to `onboard_result.json`

Use `autumn-js` SDK. The `AUTUMN_SECRET_KEY` environment variable is available. Run with `node onboard_customer.js`.

Steps to perform **in parallel where possible**:
1. Create/sync customer `user_test_001` (`"Bob Builder"`, `bob@example.com`) and `user_test_002` (`"Carol Coder"`, `carol@example.com`) using `autumn.customers.getOrCreate` with `Promise.all`.
2. After both customers are created, attach the plan `"free"` to both in parallel using `autumn.attach({ customerId, productId: 'free' })`.
3. Save results to `/home/user/myproject/onboard_result.json`:
   ```json
   {
     "customers": [
       { "customerId": "user_test_001", "planAttached": true },
       { "customerId": "user_test_002", "planAttached": true }
     ]
   }
   ```
