import { DSHCapability, DSHContext, DSHPlugin } from "../../core/types.ts";

/**
 * PluginOdooComposio — unified integration for Odoo ERP via Composio.
 *
 * Capabilities:
 *   - erp.read      : GET records from Odoo (e.g. sale.order, account.move)
 *   - erp.write     : POST/PUT mutations to Odoo
 *   - erp.comment   : Add chatter/message to an Odoo record
 *   - composio.invoke : Low-level action invocation on the connected entity
 */

export default class PluginOdooComposio implements DSHPlugin {
  name = "plugin-odoo-composio";
  version = "1.0.0";
  capabilities: DSHCapability[] = [
    "erp.read",
    "erp.write",
    "erp.comment",
    "composio.invoke",
  ];

  private composioApiKey = "";
  private composioBaseUrl = "https://backend.composio.ai/api";
  private odooEntity = "hermes_ops";        // default entity for logistics
  private odooConnectionId?: string;

  async initialize(config: Record<string, unknown>): Promise<void> {
    this.composioApiKey = String(config.composioApiKey ?? "");
    this.composioBaseUrl = String(
      config.composioBaseUrl ?? this.composioBaseUrl
    );
    this.odooEntity = String(config.entity ?? this.odooEntity);
    this.odooConnectionId = config.connectionId
      ? String(config.connectionId)
      : undefined;
    console.log(`[${this.name}] Initialized for entity ${this.odooEntity}`);
  }

  async invoke(
    capability: DSHCapability,
    context: DSHContext,
    payload: Record<string, unknown>
  ): Promise<unknown> {
    switch (capability) {
      case "erp.read":
        return this.readOdoo(payload);
      case "erp.write":
        return this.writeOdoo(payload);
      case "erp.comment":
        return this.commentOdoo(payload);
      case "composio.invoke":
        return this.invokeComposio(context, payload);
      default:
        throw new Error(`${this.name} cannot handle ${capability}`);
    }
  }

  private async readOdoo(payload: Record<string, unknown>): Promise<unknown> {
    const model = String(payload.model ?? "sale.order");
    const domain = payload.domain as any[] | undefined;
    const fields = payload.fields as string[] | undefined;
    const limit = Number(payload.limit ?? 10);

    return this.invokeComposio(
      {} as DSHContext,
      {
        action: "odoo_search_read_records",
        params: {
          model,
          domain: domain ?? [],
          fields: fields ?? ["id", "name"],
          limit,
        },
      },
      false
    );
  }

  private async writeOdoo(payload: Record<string, unknown>): Promise<unknown> {
    const model = String(payload.model ?? "sale.order");
    const values = payload.values as Record<string, unknown>;

    return this.invokeComposio(
      {} as DSHContext,
      {
        action: payload.recordId
          ? "odoo_update_record"
          : "odoo_create_record",
        params: {
          model,
          record_id: payload.recordId,
          ...values,
        },
      },
      false
    );
  }

  private async commentOdoo(payload: Record<string, unknown>): Promise<unknown> {
    const model = String(payload.model ?? "sale.order");
    const recordId = Number(payload.recordId ?? 0);
    const message = String(payload.message ?? "");

    return this.invokeComposio(
      {} as DSHContext,
      {
        action: "odoo_post_message",
        params: {
          model,
          res_id: recordId,
          body: message,
        },
      },
      false
    );
  }

  /**
   * Low-level Composio action invocation.
   */
  private async invokeComposio(
    _context: DSHContext,
    payload: Record<string, unknown>,
    log = true
  ): Promise<unknown> {
    if (!this.composioApiKey) {
      throw new Error(`${this.name} missing composioApiKey`);
    }

    const action = String(payload.action ?? "");
    const params = (payload.params ?? {}) as Record<string, unknown>;

    const url = `${this.composioBaseUrl}/v2/actions/${action}/execute`;

    const body: Record<string, unknown> = {
      connectedAccountId: this.odooConnectionId,
      entityId: this.odooEntity,
      input: params,
    };

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": this.composioApiKey,
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`Composio action ${action} failed: ${response.status} ${text}`);
    }

    const result = await response.json();

    if (log) {
      console.log(`[${this.name}] Composio ${action} result:`, JSON.stringify(result).slice(0, 200));
    }

    return result;
  }

  async shutdown(): Promise<void> {
    // Clean up any long-lived Composio sessions if needed.
  }
}
