import { PermissionEngine } from "./permissions.ts";
import { TrajectoryStore } from "./trajectory.ts";
import {
  DSHAgentDefinition,
  DSHCapability,
  DSHConfig,
  DSHContext,
  DSHMessage,
  DSHPlugin,
  DSHTrajectory,
} from "./types.ts";

/**
 * DSHToolRegistry — keeps a map of capability -> plugin.
 */
export class DSHToolRegistry {
  private map = new Map<DSHCapability, DSHPlugin>();

  register(plugin: DSHPlugin): void {
    for (const cap of plugin.capabilities) {
      this.map.set(cap, plugin);
    }
  }

  get(capability: DSHCapability): DSHPlugin | undefined {
    return this.map.get(capability);
  }
}

/**
 * DSHOrchestrator — the single entry point that loads plugins, agents,
 * permissions, and executes agent runs.
 */
export class DSHOrchestrator {
  private config: DSHConfig;
  private permissions: PermissionEngine;
  private registry = new DSHToolRegistry();
  private plugins = new Map<string, DSHPlugin>();
  private trajectoryStore: TrajectoryStore;

  constructor(config: DSHConfig) {
    this.config = config;
    this.permissions = new PermissionEngine(config.permissions);
    this.trajectoryStore = new TrajectoryStore(config.trajectory);
  }

  /**
   * Load and initialize every plugin declared in the config.
   */
  async initialize(): Promise<void> {
    for (const pluginDef of this.config.plugins) {
      const modulePath = pluginDef.path ??
        `./plugins/${pluginDef.name}/index.ts`;
      const { default: PluginClass } = await import(modulePath);
      const plugin: DSHPlugin = new PluginClass();
      await plugin.initialize(pluginDef.config);
      this.plugins.set(plugin.name, plugin);
      this.registry.register(plugin);
      console.log(`[DSH] Plugin loaded: ${plugin.name} v${plugin.version}`);
    }
  }

  /**
   * Main agent execution loop.
   */
  async run(
    agentId: string,
    userMessage: string,
    contextOverrides: Partial<DSHContext> = {}
  ): Promise<{ output: string; trajectory: DSHTrajectory }> {
    const agent = this.config.agents.find((a) => a.id === agentId);
    if (!agent) {
      throw new Error(`Agent ${agentId} not found in config`);
    }

    const requestId = crypto.randomUUID();
    const context: DSHContext = {
      requestId,
      agentRole: agent.role,
      sessionId: contextOverrides.sessionId ?? requestId,
      timestamp: new Date().toISOString(),
      metadata: contextOverrides.metadata ?? {},
      ...contextOverrides,
    };

    const trajectory = this.trajectoryStore.start(
      requestId,
      agent.id,
      agent.role
    );

    this.trajectoryStore.addStep(trajectory, {
      timestamp: new Date().toISOString(),
      agentRole: agent.role,
      agentId: agent.id,
      type: "thought",
      content: `Starting agent run for role=${agent.role} with model=${agent.model ?? "default"}`,
    });

    try {
      let messages: DSHMessage[] = [
        { role: "system", content: agent.systemPrompt },
        { role: "user", content: userMessage },
      ];

      const tools = agent.allowedTools.map(this.describeTool.bind(this));
      const maxSteps = agent.maxSteps ?? 10;
      let result = "";

      for (let step = 0; step < maxSteps; step++) {
        const response = await this.invokeCapability(
          "llm.generate",
          context,
          {
            agent,
            messages,
            model: agent.model,
            tools: tools.length > 0 ? tools : undefined,
          },
          trajectory
        );

        const responseText = String(response ?? "");

        // Try to parse response as tool_calls array.
        let toolCalls: any[] | undefined;
        try {
          const parsed = JSON.parse(responseText);
          if (Array.isArray(parsed)) {
            toolCalls = parsed;
          }
        } catch (_e) {
          // Not tool calls; treat as final text.
        }

        if (!toolCalls || toolCalls.length === 0) {
          result = responseText;
          this.trajectoryStore.addStep(trajectory, {
            timestamp: new Date().toISOString(),
            agentRole: agent.role,
            agentId: agent.id,
            type: "decision",
            content: result,
          });
          await this.trajectoryStore.finalize(trajectory, "completed", result);
          return { output: result, trajectory };
        }

        // Execute tool calls and append results to the message history.
        this.trajectoryStore.addStep(trajectory, {
          timestamp: new Date().toISOString(),
          agentRole: agent.role,
          agentId: agent.id,
          type: "thought",
          content: `Model requested ${toolCalls.length} tool call(s).`,
        });

        messages.push({
          role: "assistant",
          content: "",
        });

        for (const call of toolCalls) {
          const toolName = String(call?.function?.name ?? "");
          const argsString = String(call?.function?.arguments ?? "{}");
          let args: Record<string, unknown> = {};
          try {
            args = JSON.parse(argsString);
          } catch (_e) {
            // Invalid JSON arguments.
          }

          const toolResult = await this.executeTool(
            toolName,
            context,
            args,
            agent,
            trajectory
          );

          messages.push({
            role: "tool",
            content: JSON.stringify(toolResult),
            tool_call_id: String(call?.id ?? ""),
          });
        }
      }

      result = `Reached max steps (${maxSteps}) without a final answer.`;
      this.trajectoryStore.addStep(trajectory, {
        timestamp: new Date().toISOString(),
        agentRole: agent.role,
        agentId: agent.id,
        type: "error",
        content: result,
      });
      await this.trajectoryStore.finalize(trajectory, "failed", result);
      return { output: result, trajectory };
    } catch (error: any) {
      this.trajectoryStore.addStep(trajectory, {
        timestamp: new Date().toISOString(),
        agentRole: agent.role,
        agentId: agent.id,
        type: "error",
        content: error?.message ?? String(error),
      });
      await this.trajectoryStore.finalize(
        trajectory,
        "failed",
        undefined,
        error?.message ?? String(error)
      );
      throw error;
    }
  }

  /**
   * Public method to let an agent invoke a capability with permission checks.
   */
  async invokeCapability(
    capability: DSHCapability,
    context: DSHContext,
    payload: Record<string, unknown>,
    trajectory?: DSHTrajectory
  ): Promise<unknown> {
    if (!this.permissions.can(context.agentRole, capability, context)) {
      throw new Error(
        `Permission denied: role=${context.agentRole} cannot use ${capability}`
      );
    }

    const plugin = this.registry.get(capability);
    if (!plugin) {
      throw new Error(`No plugin registered for capability ${capability}`);
    }

    if (trajectory) {
      this.trajectoryStore.addStep(trajectory, {
        timestamp: new Date().toISOString(),
        agentRole: context.agentRole,
        agentId: (payload.agent as any)?.id ?? "unknown",
        type: "tool_call",
        content: `Invoking ${capability} on plugin ${plugin.name}`,
        payload: { capability, plugin: plugin.name },
      });
    }

    const result = await plugin.invoke(capability, context, payload);

    if (trajectory) {
      this.trajectoryStore.addStep(trajectory, {
        timestamp: new Date().toISOString(),
        agentRole: context.agentRole,
        agentId: (payload.agent as any)?.id ?? "unknown",
        type: "tool_result",
        content: `Result from ${capability}`,
        payload: { result },
      });
    }

    return result;
  }

  getAgent(role: string): DSHAgentDefinition | undefined {
    return this.config.agents.find((a) => a.role === role);
  }

  /**
   * Map a tool name requested by the LLM to a capability/plugin invocation.
   *
   * In production, this should load machine-readable tool schemas.
   */
  private async executeTool(
    toolName: string,
    context: DSHContext,
    args: Record<string, unknown>,
    agent: DSHAgentDefinition,
    trajectory?: DSHTrajectory
  ): Promise<unknown> {
    const toolMap: Record<string, DSHCapability> = {
      order_create: "erp.write",
      dispatch_search: "erp.read",
      dispatch_offer: "erp.write",
      vehicle_status: "erp.read",
      odoo_read_order: "erp.read",
      odoo_write_order: "erp.write",
      odoo_post_message: "erp.comment",
      campaign_create: "erp.write",
      lead_score: "erp.read",
      customer_segment: "erp.read",
      quote_generate: "erp.write",
      contract_create: "erp.write",
      crm_update: "erp.write",
      invoice_create: "erp.write",
      settlement_process: "erp.write",
      refund_approve: "erp.write",
      tinyfish_search: "tinyfish.search",
      n8n_run_workflow: "n8n.trigger",
      n8n_query: "n8n.trigger",
      admin_override: "composio.invoke",
      agent_regulate: "composio.invoke",
      user_suspend: "composio.invoke",
      order_cancel: "erp.write",
    };

    const capability = toolMap[toolName];
    if (!capability) {
      return { error: `Unknown tool: ${toolName}` };
    }

    // If the tool is a write operation, acquire an advisory lock where applicable.
    if (["erp.write", "composio.invoke"].includes(capability)) {
      const entityType = String(args.entityType ?? "order");
      const entityId = String(args.entityId ?? "");
      if (entityId) {
        await this.invokeCapability(
          "audit.lock",
          context,
          {
            entityType,
            entityId,
            wait: false,
          },
          trajectory
        );
      }
    }

    const result = await this.invokeCapability(
      capability,
      context,
      {
        agent,
        ...args,
      },
      trajectory
    );

    // Unlock is intentionally omitted; advisory locks should be released as soon
    // as the operation finishes. Production code may wrap this in try/finally.
    return result;
  }

  private describeTool(toolName: string): Record<string, unknown> {
    // In a real implementation, load tool schemas from a registry.
    return {
      type: "function",
      function: {
        name: toolName,
        description: `Tool: ${toolName}`,
        parameters: { type: "object", properties: {} },
      },
    };
  }

  async shutdown(): Promise<void> {
    for (const plugin of this.plugins.values()) {
      if (plugin.shutdown) await plugin.shutdown();
    }
  }
}
