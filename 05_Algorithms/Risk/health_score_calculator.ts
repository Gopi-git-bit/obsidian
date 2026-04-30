/**
 * Partnership Health Score Calculator
 *
 * Aligns with PartnershipAgreement.yaml governance weights and thresholds.
 * Designed for Supervisor Agent, n8n, and Grafana ingestion.
 */

export interface HealthMetrics {
  /** Operational: SLA compliance, fulfillment rate, dispute frequency (0-100). */
  operational: number;
  /** Financial: settlement accuracy, margin health, payout timeliness (0-100). */
  financial: number;
  /** Compliance: KYC status, data-sharing scope, audit pass rate (0-100). */
  compliance: number;
  /** Relationship: responsiveness, satisfaction, escalation rate (0-100). */
  relationship: number;
}

export interface HealthScoreThresholds {
  /** Score at or above this value can be considered for expansion. */
  expand_trigger: number;
  /** Score at or above this value should hold current scope. */
  maintain_min: number;
  /** Score at or above this value, but below maintain_min, reduces exposure. */
  reduce_exposure_min: number;
  /** Scores below this value trigger exit handling. */
  exit_trigger: number;
}

export interface HealthScoreConfig {
  weights: {
    operational: number;
    financial: number;
    compliance: number;
    relationship: number;
  };
  thresholds: HealthScoreThresholds;
  metric_minimums: {
    operational: number;
    financial: number;
    compliance: number;
    relationship: number;
  };
}

export type HealthScoreCategory = 'expand' | 'maintain' | 'reduce_exposure' | 'exit';

export interface HealthScoreResult {
  score: number;
  category: HealthScoreCategory;
  recommendations: string[];
  alerts: string[];
  metric_breakdown: Record<keyof HealthMetrics, { value: number; weighted: number }>;
  calculated_at: string;
  trace_id: string;
  version: string;
}

export interface ThresholdAction {
  action: 'EXPAND_SCOPE' | 'MAINTAIN_CURRENT' | 'REDUCE_EXPOSURE' | 'INITIATE_EXIT';
  requires_approval: boolean;
  auto_execute: boolean;
}

export const HEALTH_SCORE_CALCULATOR_VERSION = '1.0.0';

export const DEFAULT_HEALTH_CONFIG: HealthScoreConfig = {
  weights: {
    operational: 0.35,
    financial: 0.30,
    compliance: 0.20,
    relationship: 0.15,
  },
  thresholds: {
    expand_trigger: 75,
    maintain_min: 40,
    reduce_exposure_min: 20,
    exit_trigger: 20,
  },
  metric_minimums: {
    operational: 70,
    financial: 75,
    compliance: 80,
    relationship: 65,
  },
};

function clampMetric(value: number): number {
  if (!Number.isFinite(value)) {
    return 0;
  }

  return Math.max(0, Math.min(100, value));
}

function generateTraceId(): string {
  return `health-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
}

function getHealthCategory(score: number, config: HealthScoreConfig): HealthScoreCategory {
  if (score >= config.thresholds.expand_trigger) {
    return 'expand';
  }

  if (score >= config.thresholds.maintain_min) {
    return 'maintain';
  }

  if (score >= config.thresholds.reduce_exposure_min) {
    return 'reduce_exposure';
  }

  return 'exit';
}

function roundWeighted(value: number): number {
  return Math.round(value * 100) / 100;
}

export function calculateHealthScore(
  metrics: HealthMetrics,
  config: HealthScoreConfig = DEFAULT_HEALTH_CONFIG
): HealthScoreResult {
  const operational = clampMetric(metrics.operational);
  const financial = clampMetric(metrics.financial);
  const compliance = clampMetric(metrics.compliance);
  const relationship = clampMetric(metrics.relationship);

  const weightedOperational = operational * config.weights.operational;
  const weightedFinancial = financial * config.weights.financial;
  const weightedCompliance = compliance * config.weights.compliance;
  const weightedRelationship = relationship * config.weights.relationship;

  const rawScore =
    weightedOperational + weightedFinancial + weightedCompliance + weightedRelationship;
  const score = Math.round(rawScore);
  const category = getHealthCategory(score, config);

  const recommendations: string[] = [];
  const alerts: string[] = [];

  switch (category) {
    case 'expand':
      recommendations.push('Consider expanding geographic scope or order volume.');
      recommendations.push('Review contract terms for the next growth phase.');
      break;
    case 'maintain':
      recommendations.push('Maintain current scope and monitor key metrics.');
      recommendations.push('Schedule the next quarterly business review.');
      break;
    case 'reduce_exposure':
      recommendations.push('Reduce financial exposure cap immediately.');
      recommendations.push('Implement stricter SLA monitoring.');
      recommendations.push('Schedule emergency ops sync with partner.');
      alerts.push(
        `Health score below maintain threshold (${config.thresholds.maintain_min}). Reducing exposure recommended.`
      );
      break;
    case 'exit':
      recommendations.push('Initiate partnership wind-down procedure.');
      recommendations.push('Freeze new assignments and pause settlements.');
      alerts.push(
        `CRITICAL: Health score below exit threshold (${config.thresholds.exit_trigger}). Immediate action required.`
      );
      break;
  }

  if (operational < config.metric_minimums.operational) {
    alerts.push('Operational performance degraded. Review SLA breach rates and fulfillment percentage.');
  }

  if (financial < config.metric_minimums.financial) {
    alerts.push('Financial metrics below target. Verify settlement accuracy and payout delays.');
  }

  if (compliance < config.metric_minimums.compliance) {
    alerts.push('Compliance score low. Audit KYC status, data-sharing scope, and audit logs.');
  }

  if (relationship < config.metric_minimums.relationship) {
    alerts.push('Relationship score declining. Improve communication cadence and escalation resolution.');
  }

  return {
    score,
    category,
    recommendations,
    alerts,
    metric_breakdown: {
      operational: { value: operational, weighted: roundWeighted(weightedOperational) },
      financial: { value: financial, weighted: roundWeighted(weightedFinancial) },
      compliance: { value: compliance, weighted: roundWeighted(weightedCompliance) },
      relationship: { value: relationship, weighted: roundWeighted(weightedRelationship) },
    },
    calculated_at: new Date().toISOString(),
    trace_id: generateTraceId(),
    version: HEALTH_SCORE_CALCULATOR_VERSION,
  };
}

export function evaluateThresholdAction(
  score: number,
  config: HealthScoreConfig = DEFAULT_HEALTH_CONFIG
): ThresholdAction {
  const clampedScore = clampMetric(score);

  if (clampedScore >= config.thresholds.expand_trigger) {
    return { action: 'EXPAND_SCOPE', requires_approval: true, auto_execute: false };
  }

  if (clampedScore >= config.thresholds.maintain_min) {
    return { action: 'MAINTAIN_CURRENT', requires_approval: false, auto_execute: true };
  }

  if (clampedScore >= config.thresholds.reduce_exposure_min) {
    return { action: 'REDUCE_EXPOSURE', requires_approval: true, auto_execute: true };
  }

  return { action: 'INITIATE_EXIT', requires_approval: true, auto_execute: false };
}
