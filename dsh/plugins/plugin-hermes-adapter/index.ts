import {
  DSHCapability,
  DSHContext,
  DSHMessage,
  DSHPlugin,
  DSHToolCall,
} from "../core/types.ts";

/**
 * PluginHermesAdapter — connects local Hermes / DeepSeek / Docker LLM endpoint.
 *
 * Capabilities:
 *   - llm.generate  : POST to the model's /v1/chat/completions endpoint
 *   - llm.stream    : (stub) streaming response handler
 */
export default class PluginHermesAdapter implements DSHPlugin {
  name = "plugin-hermes-adapter";
  version = "1.0.0";
  capabilities: DSHCapability[] = ["llm.generate", "llm.stream"];

  private baseUrl = "";
  private apiKey = "";
  private defaultModel = "deepseek-chat";

  async initialize(config: Record<string, unknown>): Promise<void> {
    this.baseUrl = String(config.baseUrl ?? "http://localhost:8080/v1");
    this.apiKey = String(config.apiKey ?? "");
    this.defaultModel = String(config.model ?? this.defaultModel);
    console.log(`[${this.name}] Initialized with ${this.baseUrl}`);
  }

  async invoke(
    capability: DSHCapability,
    context: DSHContext,
    payload: Record<string, unknown>
  ): Promise<unknown> {
    switch (capability) {
      case "llm.generate":
        return this.generate(context, payload);
      case "llm.stream":
        return this.stream(context, payload);
      default:
        throw new Error(`${this.name} cannot handle ${capability}`);
    }
  }

  private async generate(
    _context: DSHContext,
    payload: Record<string, unknown>
  ): Promise<string> {
    const messages = (payload.messages as DSHMessage[]) ?? [];
    const model = String(payload.model ?? this.defaultModel);
    const tools = payload.tools as any[] | undefined;

    // Hermes / OpenAI-compatible chat completion shape.
    const body: Record<string, unknown> = {
      model,
      messages: messages.map((m) => ({
        role: m.role,
        content: m.content,
        name: m.name,
      })),
      temperature: 0.2,
      max_tokens: 2048,
    };

    if (tools && tools.length > 0) {
      body.tools = tools;
      body.tool_choice = "auto";
    }

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (this.apiKey) headers["Authorization"] = `Bearer ${this.apiKey}`;

    const response = await fetch(`${this.baseUrl}/chat/completions`, {
      method: "POST",
      headers,
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`Hermes LLM request failed: ${response.status} ${text}`);
    }

    const json = await response.json();
    const choice = json.choices?.[0];

    if (choice?.message?.tool_calls) {
      return JSON.stringify(choice.message.tool_calls as DSHToolCall[]);
    }

    return String(choice?.message?.content ?? "");
  }

  private async stream(
    _context: DSHContext,
    _payload: Record<string, unknown>
  ): Promise<unknown> {
    // Streaming can be implemented with a ReadableStream reader.
    console.log(`[${this.name}] Streaming not yet implemented`);
    return "";
  }
}
