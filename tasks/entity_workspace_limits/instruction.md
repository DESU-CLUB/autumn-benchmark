# Implement Multi-Tenant Workspace Usage Limits with Autumn

Build an Express.js API that manages workspace-level usage credits using Autumn's entity system. Each workspace is an Autumn entity under a parent organization customer, with its own independent credit balance.

Implement the following REST API at `/home/user/myproject`:

- `POST /workspaces` — Create a workspace entity in Autumn
- `POST /workspaces/:workspaceId/use-credits` — Check and consume workspace credits
- `GET /workspaces/:workspaceId/balance` — Fetch workspace entity balance
- `DELETE /workspaces/:workspaceId` — Delete a workspace entity

Use `autumn-js` SDK. The `AUTUMN_SECRET_KEY` environment variable is available. Server must run on port 3000.
