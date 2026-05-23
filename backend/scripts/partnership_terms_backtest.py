"""
Partnership term sheet compatibility backtest.

This script runs deterministic scenarios against Zippy's current partnership
business practice:

- driver partners default to 10% commission
- transport companies default to Rs 700/order flat fee
- partner state changes must go through documented APIs with idempotency
- payment custody and insurance distribution require regulated/legal approval
- AI can score disputes but cannot execute refunds or close cases
- loop discounts remain per-loop while invoices/refunds remain per-order
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = (
    ROOT
    / "12_Dashboards"
    / "Tableau"
    / "sample_data"
    / "sample_partnership_terms_backtest_results.csv"
)


@dataclass(frozen=True)
class PartnershipScenario:
    scenario_id: str
    partner_type: str
    description: str
    economic_model: str
    driver_commission_pct: float | None = None
    transport_company_fee_rs: int | None = None
    strategic_revenue_share_approved: bool = False
    uses_documented_api: bool = True
    has_idempotency: bool = True
    attempts_direct_db_write: bool = False
    payment_custody_model: str = "none"
    payment_legal_approved: bool = False
    insurance_distribution_model: str = "none"
    irdai_path_approved: bool = False
    ai_executes_refund: bool = False
    finance_approves_refund: bool = False
    loop_discount_once: bool = True
    per_order_invoice_refund: bool = True
    data_scope: str = "assigned_orders_only"
    has_wind_down: bool = True
    expected_decision: str = "approve"


SCENARIOS = [
    PartnershipScenario(
        scenario_id="PT-001",
        partner_type="anchor_tenant_scaas",
        description="Enterprise shipper uses SCaaS APIs with bounded SLA credits",
        economic_model="platform_fee_or_volume_commitment",
        data_scope="assigned_orders_only",
        expected_decision="approve",
    ),
    PartnershipScenario(
        scenario_id="PT-002",
        partner_type="small_fleet_operator",
        description="SFO accepts default 10% driver commission and app-only state changes",
        economic_model="driver_commission",
        driver_commission_pct=10,
        finance_approves_refund=True,
        expected_decision="approve",
    ),
    PartnershipScenario(
        scenario_id="PT-003",
        partner_type="small_fleet_operator",
        description="SFO term sheet changes default commission without signed override",
        economic_model="driver_commission",
        driver_commission_pct=14,
        expected_decision="review",
    ),
    PartnershipScenario(
        scenario_id="PT-004",
        partner_type="transport_company",
        description="Standard transport company uses Rs 700 flat service fee",
        economic_model="flat_service_fee",
        transport_company_fee_rs=700,
        expected_decision="approve",
    ),
    PartnershipScenario(
        scenario_id="PT-005",
        partner_type="transport_company",
        description="Standard transport company replaced by percentage revenue share",
        economic_model="percentage_revenue_share",
        transport_company_fee_rs=None,
        strategic_revenue_share_approved=False,
        expected_decision="review",
    ),
    PartnershipScenario(
        scenario_id="PT-006",
        partner_type="strategic_alliance",
        description="Co-opetition alliance uses approved revenue share and partner scope",
        economic_model="percentage_revenue_share",
        strategic_revenue_share_approved=True,
        data_scope="assigned_orders_only",
        expected_decision="approve",
    ),
    PartnershipScenario(
        scenario_id="PT-007",
        partner_type="payment_gateway",
        description="Licensed payment partner handles escrow and signed webhooks",
        economic_model="transaction_fee",
        payment_custody_model="regulated_partner_escrow",
        payment_legal_approved=True,
        expected_decision="approve",
    ),
    PartnershipScenario(
        scenario_id="PT-008",
        partner_type="payment_gateway",
        description="Zippy directly holds and splits funds without legal approval",
        economic_model="platform_held_funds",
        payment_custody_model="zippy_held_funds",
        payment_legal_approved=False,
        expected_decision="block",
    ),
    PartnershipScenario(
        scenario_id="PT-009",
        partner_type="insurance_partner",
        description="Insurance add-on runs through approved insurer distribution path",
        economic_model="premium_collection_partner_led",
        insurance_distribution_model="approved_partner_led",
        irdai_path_approved=True,
        expected_decision="approve",
    ),
    PartnershipScenario(
        scenario_id="PT-010",
        partner_type="insurance_partner",
        description="Term sheet says Zippy sells insurance directly without approval",
        economic_model="direct_insurance_sale",
        insurance_distribution_model="zippy_direct_sale",
        irdai_path_approved=False,
        expected_decision="block",
    ),
    PartnershipScenario(
        scenario_id="PT-011",
        partner_type="dispute_workflow",
        description="DISPUTE_AI scores case and Finance approves refund within policy",
        economic_model="sla_refund_policy",
        finance_approves_refund=True,
        expected_decision="approve",
    ),
    PartnershipScenario(
        scenario_id="PT-012",
        partner_type="dispute_workflow",
        description="DISPUTE_AI executes refund without L3 Finance approval",
        economic_model="sla_refund_policy",
        ai_executes_refund=True,
        finance_approves_refund=False,
        expected_decision="block",
    ),
    PartnershipScenario(
        scenario_id="PT-013",
        partner_type="loop_settlement",
        description="Loop discount applied once and refund/invoice remains per-order",
        economic_model="loop_discount",
        loop_discount_once=True,
        per_order_invoice_refund=True,
        expected_decision="approve",
    ),
    PartnershipScenario(
        scenario_id="PT-014",
        partner_type="loop_settlement",
        description="Loop dispute cascades refund to both legs automatically",
        economic_model="loop_discount",
        loop_discount_once=False,
        per_order_invoice_refund=False,
        expected_decision="block",
    ),
    PartnershipScenario(
        scenario_id="PT-015",
        partner_type="api_integration",
        description="Partner attempts direct database write to move order state",
        economic_model="technology_partner",
        attempts_direct_db_write=True,
        uses_documented_api=False,
        has_idempotency=False,
        expected_decision="block",
    ),
    PartnershipScenario(
        scenario_id="PT-016",
        partner_type="data_sharing",
        description="Partner requests all customer and driver data outside assigned orders",
        economic_model="data_add_on",
        data_scope="all_customer_driver_data",
        expected_decision="block",
    ),
]


def evaluate_scenario(scenario: PartnershipScenario) -> dict[str, object]:
    blockers: list[str] = []
    reviews: list[str] = []

    if scenario.attempts_direct_db_write or not scenario.uses_documented_api:
        blockers.append("state_machine_bypass")
    if not scenario.has_idempotency:
        blockers.append("missing_idempotency")
    if scenario.payment_custody_model == "zippy_held_funds" and not scenario.payment_legal_approved:
        blockers.append("unapproved_payment_custody")
    if scenario.insurance_distribution_model == "zippy_direct_sale" and not scenario.irdai_path_approved:
        blockers.append("unapproved_insurance_distribution")
    if scenario.ai_executes_refund:
        blockers.append("ai_refund_execution")
    if not scenario.loop_discount_once or not scenario.per_order_invoice_refund:
        blockers.append("loop_or_gst_isolation_broken")
    if scenario.data_scope == "all_customer_driver_data":
        blockers.append("overbroad_partner_data_access")

    if (
        scenario.economic_model == "driver_commission"
        and scenario.driver_commission_pct is not None
        and scenario.driver_commission_pct != 10
    ):
        reviews.append("driver_commission_override_required")
    if (
        scenario.partner_type == "transport_company"
        and scenario.economic_model != "flat_service_fee"
        and not scenario.strategic_revenue_share_approved
    ):
        reviews.append("transport_company_economics_override_required")
    if (
        scenario.economic_model == "flat_service_fee"
        and scenario.transport_company_fee_rs is not None
        and scenario.transport_company_fee_rs != 700
    ):
        reviews.append("transport_company_fee_override_required")
    if not scenario.has_wind_down:
        reviews.append("missing_wind_down")
    if (
        scenario.payment_custody_model not in {"none", "regulated_partner_escrow"}
        and not scenario.payment_legal_approved
    ):
        reviews.append("payment_model_review_required")
    if (
        scenario.insurance_distribution_model not in {"none", "approved_partner_led"}
        and not scenario.irdai_path_approved
    ):
        reviews.append("insurance_model_review_required")

    if blockers:
        decision = "block"
    elif reviews:
        decision = "review"
    else:
        decision = "approve"

    score = 100 - (len(blockers) * 30) - (len(reviews) * 15)
    score = max(0, score)

    return {
        "scenario_id": scenario.scenario_id,
        "partner_type": scenario.partner_type,
        "description": scenario.description,
        "economic_model": scenario.economic_model,
        "decision": decision,
        "expected_decision": scenario.expected_decision,
        "pass_fail": "pass" if decision == scenario.expected_decision else "fail",
        "compatibility_score": score,
        "blockers": ";".join(blockers) if blockers else "none",
        "review_flags": ";".join(reviews) if reviews else "none",
        "uses_documented_api": scenario.uses_documented_api,
        "has_idempotency": scenario.has_idempotency,
        "payment_custody_model": scenario.payment_custody_model,
        "insurance_distribution_model": scenario.insurance_distribution_model,
        "data_scope": scenario.data_scope,
    }


def run_backtest(output_path: Path) -> dict[str, object]:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results = [evaluate_scenario(scenario) for scenario in SCENARIOS]
    with output_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    decision_counts = {
        decision: sum(1 for row in results if row["decision"] == decision)
        for decision in ("approve", "review", "block")
    }
    failures = [row for row in results if row["pass_fail"] == "fail"]

    return {
        "rows": len(results),
        "output_path": str(output_path),
        "approve_count": decision_counts["approve"],
        "review_count": decision_counts["review"],
        "block_count": decision_counts["block"],
        "average_compatibility_score": round(
            mean(float(row["compatibility_score"]) for row in results), 2
        ),
        "fail_count": len(failures),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run partnership terms compatibility backtest.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    summary = run_backtest(args.output)
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
