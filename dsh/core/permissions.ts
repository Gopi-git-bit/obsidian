import {
  DSHAgentRole,
  DSHCapability,
  DSHContext,
  DSHPermissionRule,
} from "./types.ts";

/**
 * PermissionEngine — evaluates whether an agent role may use a capability.
 *
 * Rules are loaded from permissions.yml. Deny rules take precedence over allow.
 */
export class PermissionEngine {
  private rules: DSHPermissionRule[];

  constructor(rules: DSHPermissionRule[]) {
    this.rules = rules;
  }

  /**
   * Check if the given agent role is permitted to invoke a capability.
   * Optionally validates runtime conditions (e.g. admin-only, read-only mode).
   */
  can(
    role: DSHAgentRole,
    capability: DSHCapability,
    context?: DSHContext
  ): boolean {
    // Collect all matching rules in order.
    const matches = this.rules.filter(
      (r) => r.agentRole === role && r.capability === capability
    );

    if (matches.length === 0) {
      // Default deny.
      return false;
    }

    // Deny overrides allow.
    for (const rule of matches) {
      if (rule.effect === "deny") return false;
      if (rule.conditions && context) {
        if (!this.evaluateConditions(rule.conditions, context)) {
          return false;
        }
      }
    }

    return matches.some((r) => r.effect === "allow");
  }

  private evaluateConditions(
    conditions: Record<string, unknown>,
    context: DSHContext
  ): boolean {
    for (const [key, expected] of Object.entries(conditions)) {
      const actual = this.getValueByPath(context, key);
      if (actual !== expected) {
        return false;
      }
    }
    return true;
  }

  private getValueByPath(obj: Record<string, unknown>, path: string): unknown {
    return path.split(".").reduce<unknown>((acc, part) => {
      if (acc && typeof acc === "object") {
        return (acc as Record<string, unknown>)[part];
      }
      return undefined;
    }, obj);
  }
}
