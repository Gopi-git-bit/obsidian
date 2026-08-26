# DeepSeek Harness (DSH) — Zippy Logistics

A minimal TypeScript/Deno orchestration layer that connects the platform's AI agents to the real world:

- **Hermes** (local Docker LLM) → `plugin-hermes-adapter`
- **Composio + Odoo ERP** → `plugin-odoo-composio`
- **Supabase** (audit logs + row locks) → `plugin-supabase-audit`
- **Paperclips + TinyFish + n8n** → agent-level tool calls through the orchestrator

## Architecture

```
User / Mobile / Vercel
       │
       ▼
┌─────────────────────────────┐
│      DSH Orchestrator       │
│  (permissions + trajectory) │
└─────────────────────────────┘
       │
       ├─► plugin-hermes-adapter ──► Hermes / DeepSeek Docker endpoint
       ├─► plugin-odoo-composio ────► Composio ──► Odoo ERP
       ├─► plugin-supabase-audit ───► Supabase audit_logs + advisory locks
       └─► plugin-research ─────────► TinyFish + n8n
```

## Directory layout

```
dsh/
├── main.ts                              # CLI entry point
├── core/
│   ├── types.ts                         # Plugin contracts, config, trajectories
│   ├── orchestrator.ts                  # Agent execution loop
│   ├── permissions.ts                   # Capability allow/deny engine
│   ├── trajectory.ts                    # Decision trace storage
│   └── config.ts                        # YAML config loader
├── plugins/
│   ├── plugin-hermes-adapter/          # LLM adapter
│   ├── plugin-odoo-composio/           # ERP + Composio integration
│   ├── plugin-supabase-audit/          # Audit + row locks
│   └── plugin-research/                # TinyFish + n8n research automation
├── agents/                              # (optional) agent-specific wrappers
├── config/
│   ├── dsh.config.yml                   # Agents + plugins + trajectory config
│   └── permissions.yml                  # Capability matrix
└── trajectories/                        # Saved decision traces
```

## Quick start

### 1. Set environment variables

Create `.env` in `dsh/`:

```bash
HERMES_API_KEY=your-key-if-needed
COMPOSIO_API_KEY=your-composio-key
ODOO_CONNECTION_ID=your-odoo-connection-id
SUPABASE_URL=https://xxxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

For local runs with Deno:

```bash
deno run --allow-read --allow-env --allow-net main.ts \
  --config ./config/dsh.config.yml \
  --permissions ./config/permissions.yml \
  --agent logistics-ops \
  --prompt "Create an order from Bengaluru to Chennai, 5 tons electronics"
```

## Plugin system

Each plugin implements the `DSHPlugin` interface:

```ts
interface DSHPlugin {
  name: string;
  version: string;
  capabilities: DSHCapability[];
  initialize(config: Record<string, unknown>): Promise<void>;
  invoke(capability, context, payload): Promise<unknown>;
  shutdown?(): Promise<void>;
}
```

The orchestrator:

1. Loads all plugins declared in `dsh.config.yml`.
2. Builds a capability → plugin registry.
3. Runs the requested agent with permission checks on every tool call.
4. Saves every step to a trajectory file (local) or Supabase table.

## Permission model

Permissions are role-based and capability-based. Example:

```yaml
- agentRole: logistics-ops
  capability: erp.write
  effect: allow

- agentRole: bi-research
  capability: erp.write
  effect: deny
```

Default rule: **deny**. `effect: deny` overrides `allow`.

## Agents

| Agent | Role | Plugins | Key capabilities |
|-------|------|---------|------------------|
| `logistics-ops` | Hermes ops | Hermes, Supabase, Odoo | `llm.generate`, `audit.*`, `erp.*`, `composio.invoke` |
| `marketing-ops` | Marketing | Hermes, Supabase, Odoo | `llm.generate`, `audit.log`, `erp.*` |
| `sales-ops` | Sales | Hermes, Supabase, Odoo | `llm.generate`, `audit.log`, `erp.*` |
| `accounting-ops` | Accounting | Hermes, Supabase, Odoo | `llm.generate`, `audit.*`, `erp.*` |
| `bi-research` | Research | Hermes, Supabase, Research | `llm.generate`, `tinyfish.search`, `n8n.trigger` |
| `bi-analyst` | Analyst | Hermes, Supabase, Odoo, Research | `llm.generate`, `n8n.trigger`, `erp.read`, `erp.comment` |
| `platform-admin` | Admin | Hermes, Supabase, Odoo | All |

## Trajectory format

Every run produces a JSON file like:

```json
{
  "id": "uuid",
  "requestId": "uuid",
  "agentRole": "logistics-ops",
  "status": "completed",
  "steps": [
    { "type": "thought", "content": "..." },
    { "type": "tool_call", "content": "...", "payload": {} },
    { "type": "tool_result", "content": "..." },
    { "type": "decision", "content": "..." }
  ]
}
```

This gives full observability into every agent decision for debugging and compliance.

## Integration roadmap

1. **Hermes endpoint**: Replace `baseUrl: http://localhost:8080/v1` with your actual Docker-hosted Hermes/DeepSeek OpenAI-compatible endpoint.
2. **Composio entities**: The config uses `entity: hermes_ops`. Add a second `plugin-odoo-composio` instance with `entity: paperclips_bi` for the BI layer if you want isolation.
3. **TinyFish / n8n**: Add new capabilities and plugins for TinyFish search and n8n workflow triggers when those endpoints are available.
4. **Supabase**: The `plugin-supabase-audit` writes to the existing `public.audit_logs` table created by the Supabase migrations.

## Notes

- The harness is intentionally lightweight; it does not replace Langfuse (tracing), n8n (workflows), or Odoo (ERP). It orchestrates them.
- All writes to Odoo go through Composio so entity isolation and audit logging stay clean.
- Advisory locks in Supabase prevent concurrent agents from mutating the same order/payment record.

## Next steps

1. Wire the Vercel frontend to call DSH Edge Functions or the `main.ts` entry point.
2. Add a TinyFish plugin and n8n plugin with real HTTP clients.
3. Add a Supabase table `agent_trajectories` and update `trajectory.ts` to persist remotely.
4. Add Langfuse tracing hooks inside `orchestrator.ts`.
