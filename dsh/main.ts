import { loadConfig, loadPermissions, mergePermissions } from "./core/config.ts";
import { DSHOrchestrator } from "./core/orchestrator.ts";

/**
 * DeepSeek Harness (DSH) — Main entry point.
 *
 * Usage:
 *   deno run --allow-read --allow-env --allow-net main.ts \
 *     --config ./config/dsh.config.yml \
 *     --permissions ./config/permissions.yml \
 *     --agent logistics-ops \
 *     --prompt "Create an order from Bengaluru to Chennai, 5 tons electronics"
 */

interface CLIOptions {
  config: string;
  permissions?: string;
  agent: string;
  prompt: string;
}

function parseArgs(args: string[]): CLIOptions {
  const opts: Partial<CLIOptions> = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--config" && args[i + 1]) opts.config = args[++i];
    if (arg === "--permissions" && args[i + 1]) opts.permissions = args[++i];
    if (arg === "--agent" && args[i + 1]) opts.agent = args[++i];
    if (arg === "--prompt" && args[i + 1]) opts.prompt = args[++i];
  }

  if (!opts.config || !opts.agent || !opts.prompt) {
    throw new Error(
      "Usage: main.ts --config <path> --agent <id> --prompt <text> [--permissions <path>]"
    );
  }
  return opts as CLIOptions;
}

async function main() {
  const opts = parseArgs(Deno.args);

  let config = await loadConfig(opts.config);

  if (opts.permissions) {
    const permissions = await loadPermissions(opts.permissions);
    config = mergePermissions(config, permissions);
  }

  const orchestrator = new DSHOrchestrator(config);
  await orchestrator.initialize();

  try {
    const { output, trajectory } = await orchestrator.run(
      opts.agent,
      opts.prompt
    );
    console.log("\n=== DSH OUTPUT ===\n");
    console.log(output);
    console.log("\n=== TRAJECTORY ===");
    console.log(`Saved to: trajectories/${trajectory.requestId}-${trajectory.id}.json`);
  } finally {
    await orchestrator.shutdown();
  }
}

if (import.meta.main) {
  main().catch((err) => {
    console.error("[DSH] Fatal error:", err.message);
    Deno.exit(1);
  });
}
