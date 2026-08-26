# Zippy Logistics — Supabase Project Setup

This folder contains the **Supabase** backend setup for Zippy Logistics: migrations, Row-Level Security (RLS) policies, and Edge Functions.

> ⚠️ This setup does **not** modify the existing Django backend or business logic. It is a new, parallel SQL/Edge layer that you can run on Supabase.

## What's included

```
supabase/
├── config.toml                              # Local Supabase CLI config
├── migrations/
│   ├── 20260101000000_initial_schema.sql    # Full DB schema (25 tables, indexes, seed data)
│   ├── 20260101000001_rls_policies.sql      # Role-based access control for all tables
│   └── 20260101000002_event_and_sop_schema.sql
│       # order_event_log, sop_sections, dispatch_offers, helper functions, realtime pub
├── functions/
│   ├── _shared/
│   │   └── supabase-client.ts                # Shared service-role / anon client helpers
│   ├── order-create/
│   │   └── index.ts                          # Validates & creates an order in 'draft'
│   ├── dispatch/
│   │   └── index.ts                          # Search candidates, send offers, accept/reject
│   └── payment-hold/
│       └── index.ts                          # Create/release/check admin payment holds
```

## Prerequisites

- [Supabase CLI](https://supabase.com/docs/guides/cli) installed and logged in
- Node.js 18+ (for TypeScript/Next.js frontends)
- A Supabase project (local or cloud)

## Quick start

### 1. Configure environment

Copy `.env.example` to `.env` and fill in your project credentials:

```bash
cp supabase/.env.example supabase/.env
```

### 2. Start local Supabase (optional)

```bash
supabase start
```

### 3. Run migrations

For a linked cloud project:

```bash
supabase link --project-ref <your-project-ref>
supabase db push
```

For local development:

```bash
supabase migration up
```

### 4. Deploy Edge Functions

```bash
supabase functions deploy order-create
supabase functions deploy dispatch
supabase functions deploy payment-hold
```

### 5. Set secrets (required)

```bash
supabase secrets set SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>
supabase secrets set SUPABASE_ANON_KEY=<your-anon-key>
```

## How it fits the wider architecture

| System | Stack | Role |
|--------|-------|------|
| Database + Auth | **Supabase** (this folder) | Primary data + RLS |
| Logistics app frontends | Vercel + Next.js | Customer/Driver/Admin/TC web apps |
| Agents | Hermes / Composio (to be wired) | OMS/TMS decision automation |
| Marketing/Sales/CRM/BI | Odoo + n8n + email tools | Back-office & workflows |

## Authentication bridge

The `users` table uses `id UUID PRIMARY KEY DEFAULT uuid_generate_v4()`. When you create a Supabase Auth user, insert a matching row into `public.users` with the same `id` as `auth.users.id`. The RLS helper functions (`current_user_role`, `current_customer_id`, etc.) rely on this match.

Example:

```sql
-- After auth.user is created, run this inside a trigger or Edge Function:
INSERT INTO public.users (id, email, phone, full_name, role)
VALUES ('<auth-uid>', 'a@b.com', '+919876543210', 'Acme Logistics', 'customer');
```

You can automate this with a Postgres trigger on `auth.users`:

```sql
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email, phone, full_name, role)
  VALUES (new.id, new.email, '', '', 'customer')
  ON CONFLICT (id) DO NOTHING;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

## Edge Function examples

### Create order

```bash
curl -X POST "https://<project>.supabase.co/functions/v1/order-create" \
  -H "Authorization: Bearer <user-jwt>" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_user_id": "<auth-uid>",
    "origin_city_id": "<city-uuid>",
    "destination_city_id": "<city-uuid>",
    "origin_pincode": "560001",
    "destination_pincode": "600001",
    "material_type_id": "<material-uuid>",
    "cargo_weight_tons": 5.5
  }'
```

### Dispatch search

```bash
curl -X POST "https://<project>.supabase.co/functions/v1/dispatch" \
  -H "Authorization: Bearer <user-jwt>" \
  -H "Content-Type: application/json" \
  -d '{"action":"search","order_id":"<order-uuid>"}'
```

### Payment hold (admin only)

```bash
curl -X POST "https://<project>.supabase.co/functions/v1/payment-hold" \
  -H "Authorization: Bearer <admin-jwt>" \
  -H "Content-Type: application/json" \
  -d '{
    "action":"create",
    "payment_id":"<payment-uuid>",
    "hold_reason":"missing_pod",
    "held_amount":1500
  }'
```

## Realtime subscriptions

The migration creates a dedicated `zippy_realtime` publication with these tables:

- `orders`
- `order_event_log`
- `live_tracking`
- `vehicles`
- `notifications`
- `dispatch_offers`

Frontends can subscribe via `@supabase/supabase-js`:

```ts
supabase.channel('orders')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'orders' }, handle)
  .subscribe();
```

## Next steps

1. Wire the frontends to the new Supabase client (`lib/supabase/client.ts` samples in `SETUP_GUIDE.md`).
2. Connect Composio/Hermes agents to the `order_event_log` and `dispatch_offers` tables.
3. Add n8n webhooks that listen to `order_event_log` inserts.
4. Migrate historical Django data via `supabase db dump` or an ETL script.

## Notes

- The schema intentionally keeps the original business logic (state machine, payment rules, pricing engine) intact.
- All financial tables (`payments`, `payment_holds`, `refunds`) use RLS and admin-only mutation policies.
- Driver assignment uses the stored function `find_dispatch_candidates(...)` to keep geospatial matching close to the database.

For questions, see the main project `README.md` and `AGENTS.md`.
