import { createHash } from 'crypto';

export type ProfitSharingModelType =
  | 'contribution_weighted'
  | 'tiered_volume'
  | 'dynamic_margin';

export interface ContributionMetrics {
  /** Partner capacity as a share of total platform capacity, from 0.0 to 1.0. */
  capacity_pct: number;
  /** Revenue completed through partner resources, from 0.0 to 1.0. */
  revenue_generated_pct: number;
  /** Partner risk assumption score, from 0.0 to 1.0. */
  risk_score: number;
  /** Strategic bonus, from 0.0 to 0.5. */
  strategic_bonus_pct: number;
  /** Monthly order count for tiered-volume rules. */
  monthly_order_count?: number;
}

export interface TierConfig {
  min_orders: number;
  max_orders?: number;
  /** Partner share percentage as a decimal, e.g. 0.15 for 15%. */
  rate: number;
  /** Additional partner share percentage as a decimal. */
  bonus?: number;
}

export interface ProfitSharingRule {
  id: string;
  partnership_id: string;
  model_type: ProfitSharingModelType;
  base_commission_rate: number;
  capacity_weight?: number;
  revenue_weight?: number;
  risk_weight?: number;
  strategic_weight?: number;
  tier_config?: TierConfig[];
  min_platform_margin?: number;
  max_partner_share?: number;
  growth_bonus_threshold?: number;
  effective_from: string;
  effective_until?: string | null;
}

export interface ProfitShareResult {
  partner_share_pct: number;
  zippy_margin_pct: number;
  calculation_breakdown: Record<string, number | string | null>;
  effective_date: string;
  audit_hash: string;
}

export interface ProfitShareCalculationInput {
  partnershipId: string;
  metrics: ContributionMetrics;
  grossRevenue: number;
  grossMargin: number;
  growthMultiplier?: number;
}

export interface ProfitSharingRuleProvider {
  getActiveRule(partnershipId: string): Promise<ProfitSharingRule>;
}

const DEFAULT_CAPACITY_WEIGHT = 0.40;
const DEFAULT_REVENUE_WEIGHT = 0.30;
const DEFAULT_RISK_WEIGHT = 0.20;
const DEFAULT_STRATEGIC_WEIGHT = 0.10;
const DEFAULT_MIN_PLATFORM_MARGIN = 0.08;
const DEFAULT_MAX_PARTNER_SHARE = 0.35;
const DEFAULT_GROWTH_BONUS_THRESHOLD = 1.20;

function clamp(value: number, min: number, max: number): number {
  if (!Number.isFinite(value)) {
    return min;
  }

  return Math.max(min, Math.min(max, value));
}

function roundPct(value: number): number {
  return Number(value.toFixed(4));
}

export class ProfitShareCalculator {
  constructor(private readonly ruleProvider: ProfitSharingRuleProvider) {}

  async calculateShare(input: ProfitShareCalculationInput): Promise<ProfitShareResult> {
    const rule = await this.ruleProvider.getActiveRule(input.partnershipId);
    const grossMargin = clamp(input.grossMargin, 0, 1);
    const grossRevenue = Math.max(0, input.grossRevenue);
    const growthMultiplier = input.growthMultiplier ?? 1;

    let uncappedShare = 0;
    let breakdown: Record<string, number | string | null> = {};

    switch (rule.model_type) {
      case 'contribution_weighted': {
        const result = this.calculateContributionWeightedShare(input.metrics, rule);
        uncappedShare = result.share;
        breakdown = result.breakdown;
        break;
      }
      case 'tiered_volume': {
        const result = this.calculateTieredVolumeShare(input.metrics, rule);
        uncappedShare = result.share;
        breakdown = result.breakdown;
        break;
      }
      case 'dynamic_margin': {
        const result = this.calculateDynamicMarginShare(input.metrics, rule, grossMargin, growthMultiplier);
        uncappedShare = result.share;
        breakdown = result.breakdown;
        break;
      }
    }

    const maxPartnerShare = rule.max_partner_share ?? DEFAULT_MAX_PARTNER_SHARE;
    const minPlatformMargin = rule.min_platform_margin ?? DEFAULT_MIN_PLATFORM_MARGIN;
    const cappedShare = Math.min(uncappedShare, maxPartnerShare);
    const marginProtectedShare = Math.min(cappedShare, Math.max(0, grossMargin - minPlatformMargin));
    const partnerShare = clamp(marginProtectedShare, 0, 1);
    const zippyMargin = clamp(grossMargin - partnerShare, 0, 1);

    const calculationBreakdown = {
      model_type: rule.model_type,
      rule_id: rule.id,
      gross_revenue: grossRevenue,
      gross_margin: roundPct(grossMargin),
      uncapped_share: roundPct(uncappedShare),
      applied_cap: roundPct(maxPartnerShare),
      min_platform_margin: roundPct(minPlatformMargin),
      growth_multiplier: roundPct(growthMultiplier),
      ...breakdown,
    };

    return {
      partner_share_pct: roundPct(partnerShare),
      zippy_margin_pct: roundPct(zippyMargin),
      calculation_breakdown: calculationBreakdown,
      effective_date: new Date().toISOString(),
      audit_hash: this.generateAuditHash(input.partnershipId, partnerShare, calculationBreakdown),
    };
  }

  private calculateContributionWeightedShare(
    metrics: ContributionMetrics,
    rule: ProfitSharingRule
  ): { share: number; breakdown: Record<string, number> } {
    const capacityWeight = rule.capacity_weight ?? DEFAULT_CAPACITY_WEIGHT;
    const revenueWeight = rule.revenue_weight ?? DEFAULT_REVENUE_WEIGHT;
    const riskWeight = rule.risk_weight ?? DEFAULT_RISK_WEIGHT;
    const strategicWeight = rule.strategic_weight ?? DEFAULT_STRATEGIC_WEIGHT;

    const capacityComponent = clamp(metrics.capacity_pct, 0, 1) * capacityWeight;
    const revenueComponent = clamp(metrics.revenue_generated_pct, 0, 1) * revenueWeight;
    const riskComponent = clamp(metrics.risk_score, 0, 1) * riskWeight;
    const strategicComponent = clamp(metrics.strategic_bonus_pct, 0, 0.5) * strategicWeight;
    const contributionScore =
      capacityComponent + revenueComponent + riskComponent + strategicComponent;

    return {
      share: contributionScore * clamp(rule.base_commission_rate, 0, 1),
      breakdown: {
        capacity_component: roundPct(capacityComponent),
        revenue_component: roundPct(revenueComponent),
        risk_component: roundPct(riskComponent),
        strategic_component: roundPct(strategicComponent),
        contribution_score: roundPct(contributionScore),
        base_commission_rate: roundPct(rule.base_commission_rate),
      },
    };
  }

  private calculateTieredVolumeShare(
    metrics: ContributionMetrics,
    rule: ProfitSharingRule
  ): { share: number; breakdown: Record<string, number> } {
    const tiers = [...(rule.tier_config ?? [])].sort((a, b) => a.min_orders - b.min_orders);
    if (tiers.length === 0) {
      throw new Error(`Profit-sharing rule ${rule.id} requires tier_config.`);
    }

    const monthlyOrders = Math.max(0, Math.floor(metrics.monthly_order_count ?? 0));
    const activeTier =
      tiers.find((tier) => {
        const maxOrders = tier.max_orders ?? Number.POSITIVE_INFINITY;
        return monthlyOrders >= tier.min_orders && monthlyOrders <= maxOrders;
      }) ?? tiers[tiers.length - 1];

    const tierRate = clamp(activeTier.rate, 0, 1);
    const tierBonus = clamp(activeTier.bonus ?? 0, 0, 1);

    return {
      share: tierRate + tierBonus,
      breakdown: {
        monthly_order_count: monthlyOrders,
        tier_min_orders: activeTier.min_orders,
        tier_max_orders: activeTier.max_orders ?? -1,
        tier_rate: roundPct(tierRate),
        tier_bonus: roundPct(tierBonus),
      },
    };
  }

  private calculateDynamicMarginShare(
    metrics: ContributionMetrics,
    rule: ProfitSharingRule,
    grossMargin: number,
    growthMultiplier: number
  ): { share: number; breakdown: Record<string, number> } {
    const growthBonusThreshold = rule.growth_bonus_threshold ?? DEFAULT_GROWTH_BONUS_THRESHOLD;
    let baseShare = clamp(metrics.capacity_pct, 0, 1) * clamp(rule.base_commission_rate, 0, 1);

    if (grossMargin < 0.12) {
      baseShare = Math.min(baseShare, Math.max(0, grossMargin - DEFAULT_MIN_PLATFORM_MARGIN));
    }

    const growthBonusApplied = growthMultiplier > growthBonusThreshold ? 1 : 0;
    if (growthBonusApplied) {
      baseShare *= 1.1;
    }

    return {
      share: baseShare,
      breakdown: {
        dynamic_base_share: roundPct(baseShare),
        growth_bonus_threshold: roundPct(growthBonusThreshold),
        growth_bonus_applied: growthBonusApplied,
      },
    };
  }

  private generateAuditHash(
    partnershipId: string,
    partnerShare: number,
    breakdown: Record<string, number | string | null>
  ): string {
    return createHash('sha256')
      .update(JSON.stringify({ partnershipId, partnerShare, breakdown }))
      .digest('hex');
  }
}
