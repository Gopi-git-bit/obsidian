import { DSHCapability, DSHContext, DSHPlugin } from "../../core/types.ts";

/**
 * PluginResearch — connects TinyFish AI and n8n workflows.
 *
 * Capabilities:
 *   - tinyfish.search : POST search query to TinyFish endpoint
 *   - n8n.trigger     : POST request to an n8n webhook
 */
export default class PluginResearch implements DSHPlugin {
  name = "plugin-research";
  version = "1.0.0";
  capabilities: DSHCapability[] = ["tinyfish.search", "n8n.trigger"];

  private tinyfishBaseUrl = "";
  private tinyfishApiKey = "";
  private n8nWebhookUrl = "";
  private n8nApiKey = "";

  async initialize(config: Record<string, unknown>): Promise<void> {
    this.tinyfishBaseUrl = String(config.tinyfishBaseUrl ?? "https://api.tinyfish.ai");
    this.tinyfishApiKey = String(config.tinyfishApiKey ?? "");
    this.n8nWebhookUrl = String(config.n8nWebhookUrl ?? "");
    this.n8nApiKey = String(config.n8nApiKey ?? "");
    console.log(`[${this.name}] Initialized TinyFish + n8n clients`);
  }

  async invoke(
    capability: DSHCapability,
    _context: DSHContext,
    payload: Record<string, unknown>
  ): Promise<unknown> {
    switch (capability) {
      case "tinyfish.search":
        return this.searchTinyfish(payload);
      case "n8n.trigger":
        return this.triggerN8n(payload);
      default:
        throw new Error(`${this.name} cannot handle ${capability}`);
    }
  }

  private async searchTinyfish(payload: Record<string, unknown>): Promise<unknown> {
    const query = String(payload.query ?? "");
    if (!query) {
      throw new Error("tinyfish.search requires query");
    }

    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (this.tinyfishApiKey) headers["Authorization"] = `Bearer ${this.tinyfishApiKey}`;

    const response = await fetch(`${this.tinyfishBaseUrl}/search`, {
      method: "POST",
      headers,
      body: JSON.stringify({ query, filters: payload.filters ?? {} }),
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`TinyFish search failed: ${response.status} ${text}`);
    }

    return await response.json();
  }

  private async triggerN8n(payload: Record<string, unknown>): Promise<unknown> {
    const workflow = String(payload.workflow ?? "");
    if (!workflow) {
      throw new Error("n8n.trigger requires workflow name/id");
    }

    if (!this.n8nWebhookUrl) {
      throw new Error(`${this.name} missing n8nWebhookUrl`);
    }

    const url = this.n8nWebhookUrl.replace("{workflow}", encodeURIComponent(workflow));

    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (this.n8nApiKey) headers["X-N8N-API-KEY"] = this.n8nApiKey;

    const response = await fetch(url, {
      method: "POST",
      headers,
      body: JSON.stringify(payload.data ?? {}),
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`n8n trigger failed: ${response.status} ${text}`);
    }

    return await response.json().catch(() => ({}));
  }

  async shutdown(): Promise<void> {}
}
