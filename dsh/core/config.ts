import { parse } from "https://deno.land/std@0.224.0/yaml/mod.ts";
import { DSHConfig } from "./types.ts";

/**
 * ConfigLoader — loads dsh.config.yml and permissions.yml.
 */
export async function loadConfig(configPath: string): Promise<DSHConfig> {
  const text = await Deno.readTextFile(configPath);
  const config = parse(text) as DSHConfig;

  // Apply environment substitutions for `${VAR}` placeholders.
  const substituted = substituteEnv(config);
  return validateConfig(substituted);
}

export async function loadPermissions(
  permissionsPath: string
): Promise<DSHConfig["permissions"]> {
  const text = await Deno.readTextFile(permissionsPath);
  const doc = parse(text) as { permissions: DSHConfig["permissions"] };
  return doc.permissions ?? [];
}

function substituteEnv<T>(value: T): T {
  if (typeof value === "string") {
    return value.replace(/\$\{([^}]+)\}/g, (_, varName) => {
      return Deno.env.get(varName) ?? "";
    }) as unknown as T;
  }
  if (Array.isArray(value)) {
    return value.map(substituteEnv) as unknown as T;
  }
  if (value && typeof value === "object") {
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
      out[k] = substituteEnv(v);
    }
    return out as unknown as T;
  }
  return value;
}

function validateConfig(config: DSHConfig): DSHConfig {
  if (!config.projectId) {
    throw new Error("Config missing projectId");
  }
  if (!config.agents || config.agents.length === 0) {
    throw new Error("Config must define at least one agent");
  }
  return config;
}

export function mergePermissions(
  config: DSHConfig,
  permissions: DSHConfig["permissions"]
): DSHConfig {
  return { ...config, permissions };
}
