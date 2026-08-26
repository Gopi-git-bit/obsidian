import { DSHTrajectory, DSHTrajectoryStep } from "./types.ts";

/**
 * TrajectoryStore — persists every decision trace.
 *
 * In production, set storage to "supabase" and write to the audit/trajectory table.
 * Local mode writes JSON files to ./trajectories.
 */
export interface TrajectoryStoreConfig {
  storage: "local" | "supabase" | "s3";
  retentionDays?: number;
  supabaseUrl?: string;
  supabaseServiceKey?: string;
  localPath?: string;
}

export class TrajectoryStore {
  private config: TrajectoryStoreConfig;

  constructor(config: TrajectoryStoreConfig) {
    this.config = config;
  }

  /**
   * Start a new trajectory for the current request.
   */
  start(
    requestId: string,
    agentId: string,
    agentRole: string
  ): DSHTrajectory {
    return {
      id: this.generateId(),
      requestId,
      agentId,
      agentRole: agentRole as any,
      startedAt: new Date().toISOString(),
      status: "running",
      steps: [],
    };
  }

  /**
   * Append a step to an in-memory trajectory.
   */
  addStep(trajectory: DSHTrajectory, step: Omit<DSHTrajectoryStep, "step">): void {
    trajectory.steps.push({
      ...step,
      step: trajectory.steps.length + 1,
    });
  }

  /**
   * Mark a trajectory as completed or failed and persist it.
   */
  async finalize(
    trajectory: DSHTrajectory,
    status: "completed" | "failed",
    output?: string,
    error?: string
  ): Promise<void> {
    trajectory.endedAt = new Date().toISOString();
    trajectory.status = status;
    if (output !== undefined) trajectory.finalOutput = output;
    if (error !== undefined) trajectory.error = error;

    await this.persist(trajectory);
  }

  private async persist(trajectory: DSHTrajectory): Promise<void> {
    if (this.config.storage === "local") {
      await this.persistLocal(trajectory);
    } else if (this.config.storage === "supabase") {
      // In production, insert into a Supabase table (e.g. public.agent_trajectories).
      // This stub can be replaced with a real Supabase client call.
      console.log(
        `[TrajectoryStore] Supabase persistence stub for ${trajectory.id}`
      );
    } else {
      console.log(
        `[TrajectoryStore] S3 persistence stub for ${trajectory.id}`
      );
    }
  }

  private async persistLocal(trajectory: DSHTrajectory): Promise<void> {
    const path = this.config.localPath ?? "./trajectories";
    const fileName = `${path}/${trajectory.requestId}-${trajectory.id}.json`;

    // Ensure directory exists.
    try {
      await Deno.mkdir(path, { recursive: true });
    } catch (_e) {
      // Directory may already exist.
    }

    await Deno.writeTextFile(
      fileName,
      JSON.stringify(trajectory, null, 2)
    );
  }

  private generateId(): string {
    return crypto.randomUUID();
  }
}
