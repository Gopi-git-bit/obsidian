import { createClient, SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2.45.0";
import { DSHCapability, DSHContext, DSHPlugin } from "../../core/types.ts";

/**
 * PluginSupabaseAudit — handles audit logging and "row locks" via Supabase.
 *
 * Capabilities:
 *   - audit.log   : insert into public.audit_logs
 *   - audit.lock  : advisory lock around a critical operation
 */
export default class PluginSupabaseAudit implements DSHPlugin {
  name = "plugin-supabase-audit";
  version = "1.0.0";
  capabilities: DSHCapability[] = ["audit.log", "audit.lock"];

  private supabase?: SupabaseClient;

  async initialize(config: Record<string, unknown>): Promise<void> {
    const url = String(config.supabaseUrl ?? "");
    const key = String(config.serviceRoleKey ?? "");

    if (!url || !key) {
      throw new Error(`${this.name} requires supabaseUrl and serviceRoleKey`);
    }

    this.supabase = createClient(url, key, {
      auth: { persistSession: false, autoRefreshToken: false },
    });

    console.log(`[${this.name}] Connected to Supabase at ${url}`);
  }

  async invoke(
    capability: DSHCapability,
    context: DSHContext,
    payload: Record<string, unknown>
  ): Promise<unknown> {
    if (!this.supabase) {
      throw new Error(`${this.name} not initialized`);
    }

    switch (capability) {
      case "audit.log":
        return this.log(context, payload);
      case "audit.lock":
        return this.lock(context, payload);
      default:
        throw new Error(`${this.name} cannot handle ${capability}`);
    }
  }

  private async log(
    context: DSHContext,
    payload: Record<string, unknown>
  ): Promise<unknown> {
    const entityType = String(payload.entityType ?? "agent_decision");
    const entityId = String(payload.entityId ?? "00000000-0000-0000-0000-000000000000");
    const action = String(payload.action ?? "run");

    const { error } = await this.supabase!.from("audit_logs").insert({
      entity_type: entityType,
      entity_id: entityId,
      action,
      performed_by: context.userId ?? null,
      performed_by_type: "api",
      old_values: payload.oldValues ?? null,
      new_values: payload.newValues ?? null,
    });

    if (error) {
      throw new Error(`Audit log insert failed: ${error.message}`);
    }

    return { logged: true };
  }

  /**
   * Acquires a Postgres advisory lock for the given entity.
   * Returns true if the lock was acquired, false otherwise.
   */
  private async lock(
    _context: DSHContext,
    payload: Record<string, unknown>
  ): Promise<boolean> {
    const entityType = String(payload.entityType ?? "order");
    const entityId = String(payload.entityId ?? "");
    const lockKey = this.hashLockKey(entityType, entityId);
    const wait = Boolean(payload.wait ?? true);

    // pg_try_advisory_lock is non-blocking; pg_advisory_lock blocks.
    const fn = wait ? "pg_advisory_lock" : "pg_try_advisory_lock";

    const { data, error } = await this.supabase!.rpc(fn, { key: lockKey });

    if (error) {
      throw new Error(`Advisory lock failed: ${error.message}`);
    }

    return Boolean(data);
  }

  /**
   * Releases a previously acquired advisory lock.
   */
  async unlock(
    _context: DSHContext,
    payload: Record<string, unknown>
  ): Promise<boolean> {
    const entityType = String(payload.entityType ?? "order");
    const entityId = String(payload.entityId ?? "");
    const lockKey = this.hashLockKey(entityType, entityId);

    const { data, error } = await this.supabase!.rpc("pg_advisory_unlock", {
      key: lockKey,
    });

    if (error) {
      throw new Error(`Advisory unlock failed: ${error.message}`);
    }

    return Boolean(data);
  }

  private hashLockKey(entityType: string, entityId: string): number {
    // Combine entity type and id into a 64-bit signed integer key.
    // Simple djb2 hash; collision probability is acceptable for advisory locks.
    const str = `${entityType}:${entityId}`;
    let hash = 5381;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) + hash + str.charCodeAt(i)) & 0x7fffffff;
    }
    return hash;
  }

  async shutdown(): Promise<void> {
    // No persistent session to clean up.
  }
}
