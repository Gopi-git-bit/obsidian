import {
  ContributionMetrics,
  ProfitShareCalculator,
  ProfitSharingRule,
  ProfitSharingRuleProvider,
} from '../ProfitShareCalculator';

class StaticRuleProvider implements ProfitSharingRuleProvider {
  constructor(private readonly rule: ProfitSharingRule) {}

  async getActiveRule(_partnershipId: string): Promise<ProfitSharingRule> {
    return this.rule;
  }
}

function createCalculator(rule: ProfitSharingRule): ProfitShareCalculator {
  return new ProfitShareCalculator(new StaticRuleProvider(rule));
}

function baseRule(overrides: Partial<ProfitSharingRule> = {}): ProfitSharingRule {
  return {
    id: 'rule-001',
    partnership_id: 'partner-001',
    model_type: 'contribution_weighted',
    base_commission_rate: 0.15,
    capacity_weight: 0.40,
    revenue_weight: 0.30,
    risk_weight: 0.20,
    strategic_weight: 0.10,
    min_platform_margin: 0.08,
    max_partner_share: 0.35,
    growth_bonus_threshold: 1.20,
    effective_from: '2026-01-01T00:00:00Z',
    effective_until: null,
    ...overrides,
  };
}

const baseMetrics: ContributionMetrics = {
  capacity_pct: 0.25,
  revenue_generated_pct: 0.30,
  risk_score: 1.0,
  strategic_bonus_pct: 0.15,
  monthly_order_count: 150,
};

describe('ProfitShareCalculator', () => {
  it('calculates contribution-weighted partner share', async () => {
    const result = await createCalculator(baseRule()).calculateShare({
      partnershipId: 'partner-001',
      metrics: baseMetrics,
      grossRevenue: 1_000_000,
      grossMargin: 0.40,
      growthMultiplier: 1.0,
    });

    // (0.25*0.40)+(0.30*0.30)+(1.0*0.20)+(0.15*0.10) = 0.405
    // 0.405 * 0.15 = 0.06075
    expect(result.partner_share_pct).toBeCloseTo(0.0608, 4);
    expect(result.zippy_margin_pct).toBeCloseTo(0.3392, 4);
    expect(result.calculation_breakdown.contribution_score).toBeCloseTo(0.405, 4);
  });

  it('calculates tiered-volume partner share as the final tier rate plus bonus', async () => {
    const rule = baseRule({
      model_type: 'tiered_volume',
      tier_config: [
        { min_orders: 0, max_orders: 50, rate: 0.18, bonus: 0 },
        { min_orders: 51, max_orders: 200, rate: 0.15, bonus: 0.02 },
        { min_orders: 201, max_orders: 1000, rate: 0.12, bonus: 0.04 },
      ],
    });

    const result = await createCalculator(rule).calculateShare({
      partnershipId: 'partner-001',
      metrics: { ...baseMetrics, monthly_order_count: 150 },
      grossRevenue: 1_000_000,
      grossMargin: 0.40,
      growthMultiplier: 1.0,
    });

    expect(result.partner_share_pct).toBeCloseTo(0.17, 4);
    expect(result.calculation_breakdown.tier_rate).toBe(0.15);
    expect(result.calculation_breakdown.tier_bonus).toBe(0.02);
  });

  it('falls back to the highest tier when monthly orders exceed configured ranges', async () => {
    const rule = baseRule({
      model_type: 'tiered_volume',
      tier_config: [
        { min_orders: 0, max_orders: 50, rate: 0.18, bonus: 0 },
        { min_orders: 51, max_orders: 200, rate: 0.15, bonus: 0.02 },
      ],
    });

    const result = await createCalculator(rule).calculateShare({
      partnershipId: 'partner-001',
      metrics: { ...baseMetrics, monthly_order_count: 500 },
      grossRevenue: 1_000_000,
      grossMargin: 0.40,
      growthMultiplier: 1.0,
    });

    expect(result.partner_share_pct).toBeCloseTo(0.17, 4);
    expect(result.calculation_breakdown.tier_min_orders).toBe(51);
  });

  it('calculates dynamic-margin share with growth bonus applied', async () => {
    const result = await createCalculator(baseRule({ model_type: 'dynamic_margin' })).calculateShare({
      partnershipId: 'partner-001',
      metrics: baseMetrics,
      grossRevenue: 1_000_000,
      grossMargin: 0.40,
      growthMultiplier: 1.3,
    });

    // 0.25 * 0.15 = 0.0375; growth bonus = 0.04125.
    expect(result.partner_share_pct).toBeCloseTo(0.0413, 4);
    expect(result.calculation_breakdown.growth_bonus_applied).toBe(1);
  });

  it('enforces minimum platform margin protection', async () => {
    const result = await createCalculator(baseRule({ min_platform_margin: 0.25 })).calculateShare({
      partnershipId: 'partner-001',
      metrics: { ...baseMetrics, capacity_pct: 0.9, risk_score: 1.0 },
      grossRevenue: 1_000_000,
      grossMargin: 0.30,
      growthMultiplier: 1.0,
    });

    expect(result.partner_share_pct).toBeLessThanOrEqual(0.05);
    expect(result.zippy_margin_pct).toBeGreaterThanOrEqual(0.25);
  });

  it('enforces max partner share cap', async () => {
    const result = await createCalculator(baseRule({ max_partner_share: 0.05 })).calculateShare({
      partnershipId: 'partner-001',
      metrics: baseMetrics,
      grossRevenue: 1_000_000,
      grossMargin: 0.50,
      growthMultiplier: 1.0,
    });

    expect(result.partner_share_pct).toBeLessThanOrEqual(0.05);
  });

  it('clamps invalid contribution inputs safely', async () => {
    const badMetrics: ContributionMetrics = {
      capacity_pct: 1.5,
      revenue_generated_pct: -0.2,
      risk_score: 2.0,
      strategic_bonus_pct: 0.8,
    };

    const result = await createCalculator(baseRule()).calculateShare({
      partnershipId: 'partner-001',
      metrics: badMetrics,
      grossRevenue: 1_000_000,
      grossMargin: 0.40,
      growthMultiplier: 1.0,
    });

    expect(result.partner_share_pct).toBeGreaterThan(0);
    expect(result.calculation_breakdown.capacity_component).toBe(0.4);
    expect(result.calculation_breakdown.revenue_component).toBe(0);
  });

  it('throws for tiered-volume rules without tier config', async () => {
    await expect(
      createCalculator(baseRule({ model_type: 'tiered_volume' })).calculateShare({
        partnershipId: 'partner-001',
        metrics: baseMetrics,
        grossRevenue: 1_000_000,
        grossMargin: 0.40,
        growthMultiplier: 1.0,
      })
    ).rejects.toThrow('requires tier_config');
  });

  it('generates deterministic audit hash for identical calculation inputs', async () => {
    const calculator = createCalculator(baseRule());
    const input = {
      partnershipId: 'partner-001',
      metrics: baseMetrics,
      grossRevenue: 1_000_000,
      grossMargin: 0.40,
      growthMultiplier: 1.0,
    };

    const first = await calculator.calculateShare(input);
    const second = await calculator.calculateShare(input);

    expect(first.audit_hash).toMatch(/^[a-f0-9]{64}$/);
    expect(first.audit_hash).toBe(second.audit_hash);
  });

  it('handles zero gross margin safely', async () => {
    const result = await createCalculator(baseRule()).calculateShare({
      partnershipId: 'partner-001',
      metrics: baseMetrics,
      grossRevenue: 1_000_000,
      grossMargin: 0,
      growthMultiplier: 1.0,
    });

    expect(result.partner_share_pct).toBe(0);
    expect(result.zippy_margin_pct).toBe(0);
  });
});
