/**
 * DeepSeek Harness (DSH) — Core Types
 *
 * Defines the plugin contract, agent definitions, permissions, messages,
 * tool calls, and decision trajectories.
 */

export type DSHAgentRole =
  | "logistics-ops"      // Layer A: Hermes-driven operations
  | "marketing-ops"
  | "sales-ops"
  | "accounting-ops"
  | "bi-research"        // Layer B: Paperclips-driven intelligence
  | "bi-analyst"
  | "platform-admin";

export type DSHCapability =
  | "llm.generate"
  | "llm.stream"
  | "audit.log"
  | "audit.lock"
  | "erp.read"
  | "erp.write"
  | "erp.comment"
  | "composio.invoke"
  | "n8n.trigger"
  | "tinyfish.search"
  | "trajectory.save"
  | "trajectory.load";

export interface DSHContext {
  requestId: string;
  agentRole: DSHAgentRole;
  userId?: string;
  sessionId: string;
  timestamp: string;
  metadata: Record<string, unknown>;
}

export interface DSHMessage {
  role: "system" | "user" | "assistant" | "tool";
  content: string;
  name?: string;       // for tool messages
  tool_call_id?: string;
}

export interface DSHToolCall {
  id: string;
  type: "function";
  function: {
    name: string;
    arguments: string; // JSON string
  };
}

export interface DSHToolResult {
  tool_call_id: string;
  role: "tool";
  content: string;
}

export interface DSHPlugin {
  name: string;
  version: string;
  capabilities: DSHCapability[];
  initialize(config: Record<string, unknown>): Promise<void>;
  invoke(
    capability: DSHCapability,
    context: DSHContext,
    payload: Record<string, unknown>
  ): Promise<unknown>;
  shutdown?(): Promise<void>;
}

export interface DSHAgentDefinition {
  id: string;
  role: DSHAgentRole;
  displayName: string;
  description: string;
  model?: string;              // e.g. "deepseek-chat", "hermes-2-pro", "tinyfish"
  capabilities: DSHCapability[];
  allowedTools: string[];      // tool name allow-list
  systemPrompt: string;
  plugins: string[];         // plugin names to load
  maxSteps?: number;
}

export interface DSHPermissionRule {
  agentRole: DSHAgentRole;
  capability: DSHCapability;
  effect: "allow" | "deny";
  conditions?: Record<string, unknown>;
}

export interface DSHConfig {
  projectId: string;
  environment: "development" | "staging" | "production";
  plugins: Array<{
    name: string;
    path?: string;
    config: Record<string, unknown>;
  }>;
  agents: DSHAgentDefinition[];
  permissions: DSHPermissionRule[];
  trajectory: {
    enabled: boolean;
    storage: "local" | "supabase" | "s3";
    retentionDays: number;
  };
}

export interface DSHTrajectoryStep {
  step: number;
  timestamp: string;
  agentRole: DSHAgentRole;
  agentId: string;
  type: "thought" | "tool_call" | "tool_result" | "observation" | "decision" | "error";
  content: string;
  payload?: Record<string, unknown>;
}

export interface DSHTrajectory {
  id: string;
  requestId: string;
  agentRole: DSHAgentRole;
  agentId: string;
  startedAt: string;
  endedAt?: string;
  status: "running" | "completed" | "failed";
  steps: DSHTrajectoryStep[];
  finalOutput?: string;
  error?: string;
}

export interface DSHOrchestratorOptions {
  configPath: string;
  permissionsPath?: string;
  overrideEnv?: Record<string, string>;
}
