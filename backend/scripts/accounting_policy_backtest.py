"""
Broker-model accounting policy backtest.

This script runs deterministic scenarios against Zippy's default
agent/broker accounting policy:

- gross freight is a collection liability, not revenue
- commission revenue is recognized only after POD + OTP
- GST is calculated on commission/platform fee, not gross freight
- driver/vehicle-owner payable is created only after completion evidence clears
- disputes, contract-risk, and month-end cut-off create holds/reviews
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = (
    ROOT
    / "12_Dashboards"
    / "Tableau"
    / "sample_data"
    / "sample_accounting_policy_backtest_results.csv"
)

MONEY = Decimal("0.01")
GST_RATE = Decimal("0.18")


@dataclass(frozen=True)
class AccountingScenario:
    scenario_id: str
    description: str
    gross_collection: Decimal
    driver_payable: Decimal
    commission: Decimal
    pod_verified: bool
    otp_verified: bool
    dispute_open: bool = False
    fraud_hold: bool = False
    cancellation_hold: bool = False
    contract_supports_broker: bool = True
    zippy_primary_delivery_obligor: bool = False
    zippy_owns_vehicle: bool = False
    period_end_day: int = 31
    pod_day: int | None = None
    otp_day: int | None = None
    attempted_gross_revenue_posting: bool = False
    expected_result: str = "pass"


def money(value: str) -> Decimal:
    return Decimal(value).quantize(MONEY)


SCENARIOS = [
    AccountingScenario(
        scenario_id="ACCT-001",
        description="Clean prepaid broker transaction after POD and OTP",
        gross_collection=money("50900"),
        driver_payable=money("45000"),
        commission=money("5000"),
        pod_verified=True,
        otp_verified=True,
        pod_day=20,
        otp_day=20,
        expected_result="pass",
    ),
    AccountingScenario(
        scenario_id="ACCT-002",
        description="Payment received but no POD or OTP",
        gross_collection=money("50900"),
        driver_payable=money("45000"),
        commission=money("5000"),
        pod_verified=False,
        otp_verified=False,
        expected_result="pass",
    ),
    AccountingScenario(
        scenario_id="ACCT-003",
        description="POD verified but OTP missing",
        gross_collection=money("50900"),
        driver_payable=money("45000"),
        commission=money("5000"),
        pod_verified=True,
        otp_verified=False,
        pod_day=28,
        expected_result="pass",
    ),
    AccountingScenario(
        scenario_id="ACCT-004",
        description="POD and OTP complete but driver dispute open",
        gross_collection=money("50900"),
        driver_payable=money("45000"),
        commission=money("5000"),
        pod_verified=True,
        otp_verified=True,
        dispute_open=True,
        pod_day=18,
        otp_day=18,
        expected_result="pass",
    ),
    AccountingScenario(
        scenario_id="ACCT-005",
        description="Gross freight incorrectly attempted as revenue",
        gross_collection=money("50900"),
        driver_payable=money("45000"),
        commission=money("5000"),
        pod_verified=True,
        otp_verified=True,
        pod_day=12,
        otp_day=12,
        attempted_gross_revenue_posting=True,
        expected_result="blocked",
    ),
    AccountingScenario(
        scenario_id="ACCT-006",
        description="Contract wording does not support broker model",
        gross_collection=money("50900"),
        driver_payable=money("45000"),
        commission=money("5000"),
        pod_verified=True,
        otp_verified=True,
        contract_supports_broker=False,
        pod_day=10,
        otp_day=10,
        expected_result="review",
    ),
    AccountingScenario(
        scenario_id="ACCT-007",
        description="POD before month-end but OTP after month-end",
        gross_collection=money("50900"),
        driver_payable=money("45000"),
        commission=money("5000"),
        pod_verified=True,
        otp_verified=True,
        pod_day=30,
        otp_day=32,
        expected_result="pass",
    ),
    AccountingScenario(
        scenario_id="ACCT-008",
        description="Zippy owns vehicle for transaction, principal review needed",
        gross_collection=money("5900"),
        driver_payable=money("0"),
        commission=money("5000"),
        pod_verified=True,
        otp_verified=True,
        zippy_owns_vehicle=True,
        zippy_primary_delivery_obligor=True,
        pod_day=16,
        otp_day=16,
        expected_result="review",
    ),
]


def q(value: Decimal) -> Decimal:
    return value.quantize(MONEY, rounding=ROUND_HALF_UP)


def evaluate_scenario(scenario: AccountingScenario) -> dict[str, object]:
    gross = scenario.gross_collection
    driver_payable = scenario.driver_payable
    commission = scenario.commission
    gst_on_commission = q(commission * GST_RATE)
    required_liability = q(driver_payable + commission + gst_on_commission)
    liability_reconciles = gross == required_liability

    classification = "AGENT"
    revenue_presentation = "NET_COMMISSION"
    review_reasons: list[str] = []
    holds: list[str] = []

    if not scenario.contract_supports_broker:
        review_reasons.append("contract_wording_not_broker_safe")
    if scenario.zippy_primary_delivery_obligor:
        review_reasons.append("zippy_primary_delivery_obligor")
    if scenario.zippy_owns_vehicle:
        review_reasons.append("zippy_owns_vehicle")

    if review_reasons:
        classification = "REVIEW_REQUIRED"
        revenue_presentation = "BLOCK_UNTIL_REVIEW"

    if not scenario.pod_verified:
        holds.append("pod_missing")
    if not scenario.otp_verified:
        holds.append("otp_missing")
    if scenario.dispute_open:
        holds.append("dispute_open")
    if scenario.fraud_hold:
        holds.append("fraud_hold")
    if scenario.cancellation_hold:
        holds.append("cancellation_hold")
    if scenario.attempted_gross_revenue_posting:
        holds.append("gross_revenue_error")
    if not liability_reconciles:
        holds.append("collection_split_mismatch")

    period_cutoff_passed = (
        scenario.pod_day is not None
        and scenario.otp_day is not None
        and scenario.pod_day <= scenario.period_end_day
        and scenario.otp_day <= scenario.period_end_day
    )

    recognize_commission = (
        classification == "AGENT"
        and scenario.pod_verified
        and scenario.otp_verified
        and not scenario.dispute_open
        and not scenario.fraud_hold
        and not scenario.cancellation_hold
        and not scenario.attempted_gross_revenue_posting
        and period_cutoff_passed
    )

    create_driver_payable = (
        classification == "AGENT"
        and scenario.pod_verified
        and scenario.otp_verified
        and not scenario.dispute_open
        and not scenario.attempted_gross_revenue_posting
    )

    revenue_amount = commission if recognize_commission else Decimal("0")
    taxable_value = commission if recognize_commission else Decimal("0")
    output_gst = gst_on_commission if recognize_commission else Decimal("0")
    revenue_ratio = (revenue_amount / gross) if gross else Decimal("0")

    if scenario.attempted_gross_revenue_posting:
        actual_result = "blocked"
    elif review_reasons:
        actual_result = "review"
    else:
        actual_result = "pass"

    pass_fail = "pass" if actual_result == scenario.expected_result else "fail"

    return {
        "scenario_id": scenario.scenario_id,
        "description": scenario.description,
        "principal_agent_status": classification,
        "revenue_presentation": revenue_presentation,
        "gross_collection": q(gross),
        "customer_collection_liability_initial": q(gross),
        "driver_payable_input": q(driver_payable),
        "commission_input": q(commission),
        "gst_on_commission": gst_on_commission,
        "required_liability_after_split": required_liability,
        "liability_reconciles": liability_reconciles,
        "recognize_commission": recognize_commission,
        "recognized_revenue": q(revenue_amount),
        "zippy_taxable_value": q(taxable_value),
        "output_gst_posted": q(output_gst),
        "create_driver_payable": create_driver_payable,
        "driver_payable_posted": q(driver_payable if create_driver_payable else Decimal("0")),
        "period_cutoff_passed": period_cutoff_passed,
        "holds": "|".join(holds) if holds else "none",
        "review_reasons": "|".join(review_reasons) if review_reasons else "none",
        "attempted_gross_revenue_posting": scenario.attempted_gross_revenue_posting,
        "revenue_to_gross_ratio": q(revenue_ratio),
        "expected_result": scenario.expected_result,
        "actual_result": actual_result,
        "pass_fail": pass_fail,
    }


def run_backtest(output_path: Path) -> dict[str, object]:
    rows = [evaluate_scenario(scenario) for scenario in SCENARIOS]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    pass_count = sum(1 for row in rows if row["pass_fail"] == "pass")
    block_count = sum(1 for row in rows if row["actual_result"] == "blocked")
    review_count = sum(1 for row in rows if row["actual_result"] == "review")
    recognized_revenues = [Decimal(str(row["recognized_revenue"])) for row in rows]

    return {
        "rows": len(rows),
        "pass_count": pass_count,
        "fail_count": len(rows) - pass_count,
        "blocked_count": block_count,
        "review_count": review_count,
        "average_recognized_revenue": q(mean(recognized_revenues)),
        "output_path": str(output_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run accounting policy backtest.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    summary = run_backtest(args.output)
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
