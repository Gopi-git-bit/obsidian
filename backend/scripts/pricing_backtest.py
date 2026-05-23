"""
Pricing engine proxy backtest for Zippy corridor seed lanes.

This script validates the enhanced pricing engine against the best lane-level
proxy data currently available in the vault. It is intentionally deterministic:
no live market data, no random sampling, and no network access.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.services.pricing_service import DynamicPricingEngine


DEFAULT_INPUT = (
    ROOT
    / "12_Dashboards"
    / "Tableau"
    / "sample_data"
    / "sample_corridor_opportunity_scores.csv"
)
DEFAULT_OUTPUT = (
    ROOT
    / "12_Dashboards"
    / "Tableau"
    / "sample_data"
    / "sample_pricing_backtest_results.csv"
)

LANE_DISTANCES_KM = {
    "tiruppur:chennai:garments": 465,
    "chennai:tiruppur:textiles": 465,
    "coimbatore:chennai:engineering": 510,
    "chennai:coimbatore:mixed": 510,
    "erode:chennai:textiles": 400,
    "karur:chennai:home_textiles": 390,
    "namakkal:chennai:poultry_industrial": 375,
    "hosur:chennai:auto_components": 310,
    "hosur:coimbatore:industrial": 330,
    "coimbatore:tuticorin_via_madurai:export": 380,
}

CARGO_PROFILE = {
    "garments": {"vehicle_category": "HCV", "weight_kg": 9000, "service_type": "standard"},
    "textiles": {"vehicle_category": "HCV", "weight_kg": 9000, "service_type": "standard"},
    "engineering": {"vehicle_category": "HCV", "weight_kg": 12000, "service_type": "standard"},
    "mixed": {"vehicle_category": "HCV", "weight_kg": 10000, "service_type": "standard"},
    "auto_components": {"vehicle_category": "HCV", "weight_kg": 11000, "service_type": "express"},
    "industrial": {"vehicle_category": "HCV", "weight_kg": 11000, "service_type": "standard"},
    "export": {"vehicle_category": "Trailer", "weight_kg": 14000, "service_type": "express"},
    "poultry_industrial": {"vehicle_category": "HCV", "weight_kg": 10000, "service_type": "standard"},
    "home_textiles": {"vehicle_category": "HCV", "weight_kg": 9000, "service_type": "standard"},
}


def _as_int(row: dict[str, str], key: str) -> int:
    return int(float(row[key]))


def _as_bool(row: dict[str, str], key: str) -> bool:
    return row.get(key, "").strip().lower() == "true"


def infer_cargo_profile(lane_id: str) -> dict[str, object]:
    for token, profile in CARGO_PROFILE.items():
        if token in lane_id:
            return profile
    return {"vehicle_category": "HCV", "weight_kg": 10000, "service_type": "standard"}


def infer_lane_viability(backhaul_score: int) -> str:
    if backhaul_score >= 11:
        return "highly_balanced"
    if backhaul_score >= 9:
        return "moderately_balanced"
    if backhaul_score >= 7:
        return "unbalanced_origin_heavy"
    return "remote_low_demand"


def infer_route_difficulty(row: dict[str, str]) -> float:
    complexity_score = _as_int(row, "complexity_score")
    competition_score = _as_int(row, "competition_score")
    hard_gate = _as_bool(row, "hard_gate_flag")
    route_shape = row.get("route_shape", "")

    difficulty = 25 + ((10 - complexity_score) * 5) + max(0, 8 - competition_score) * 2
    if route_shape == "port_linked":
        difficulty += 10
    if hard_gate:
        difficulty += 15
    return max(0, min(100, difficulty))


def build_pricing_params(row: dict[str, str]) -> dict[str, object]:
    lane_id = row["lane_id"]
    profile = infer_cargo_profile(lane_id)
    backhaul_score = _as_int(row, "backhaul_score")
    demand_score = _as_int(row, "demand_score")
    supply_score = _as_int(row, "supply_score")

    return {
        "weight_kg": profile["weight_kg"],
        "distance_km": LANE_DISTANCES_KM.get(lane_id, 400),
        "vehicle_category": profile["vehicle_category"],
        "origin_city": row["origin_city"],
        "destination_city": row["destination_city"].split(" via ")[0],
        "service_type": profile["service_type"],
        "customer_type": "medium",
        "demand": max(demand_score, 1),
        "supply": max(supply_score, 1),
        "is_remote": backhaul_score <= 6,
        "is_hill": False,
        "is_congested": _as_int(row, "complexity_score") <= 6,
        "is_festival": False,
        "route_difficulty_score": infer_route_difficulty(row),
        "lane_viability": infer_lane_viability(backhaul_score),
        "return_load_probability": min(0.95, max(0.05, backhaul_score / 12)),
    }


def classify_price_read(row: dict[str, str], quote: dict[str, object]) -> str:
    rate_per_km = float(quote["breakdown_per_km"])
    lane_viability = quote["deadhead_lane_viability"]["lane_viability"]
    hard_gate = _as_bool(row, "hard_gate_flag")
    recommendation = row["recommendation"]

    if hard_gate and recommendation == "validate_manually":
        return "correctly_gated"
    if lane_viability == "remote_low_demand" and rate_per_km >= 45:
        return "deadhead_risk_priced"
    if recommendation == "build_later" and rate_per_km >= 40:
        return "weak_lane_not_underpriced"
    if recommendation == "validate_manually" and rate_per_km < 65:
        return "commercially_testable"
    return "review"


def run_backtest(input_path: Path, output_path: Path) -> dict[str, object]:
    engine = DynamicPricingEngine(use_ml=False)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))

    results: list[dict[str, object]] = []
    for row in rows:
        params = build_pricing_params(row)
        quote = engine.calculate_price(params)
        results.append(
            {
                "lane_id": row["lane_id"],
                "origin_city": row["origin_city"],
                "destination_city": row["destination_city"],
                "recommendation": row["recommendation"],
                "hard_gate_flag": row["hard_gate_flag"],
                "distance_km": params["distance_km"],
                "vehicle_category": params["vehicle_category"],
                "route_difficulty_score": quote["route_difficulty"]["score"],
                "route_difficulty_tier": quote["route_difficulty"]["tier"],
                "route_difficulty_surcharge_pct": quote["route_difficulty"]["surcharge_pct"],
                "density_multiplier": quote["urbanization_density"]["density_multiplier"],
                "lane_viability": quote["deadhead_lane_viability"]["lane_viability"],
                "deadhead_surcharge_pct": quote["deadhead_lane_viability"]["deadhead_surcharge_pct"],
                "surge_multiplier": quote["surge_multiplier"],
                "service_type": quote["service_type"],
                "subtotal": quote["subtotal"],
                "platform_fee": quote["platform_fee"],
                "gst_amount": quote["gst_amount"],
                "final_price": quote["final_price"],
                "rate_per_km": quote["breakdown_per_km"],
                "price_read": classify_price_read(row, quote),
            }
        )

    fieldnames = list(results[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    review_count = sum(1 for row in results if row["price_read"] == "review")
    return {
        "rows": len(results),
        "output_path": str(output_path),
        "average_rate_per_km": round(mean(float(row["rate_per_km"]) for row in results), 2),
        "average_rds": round(mean(float(row["route_difficulty_score"]) for row in results), 2),
        "review_count": review_count,
        "pass_count": len(results) - review_count,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run pricing proxy backtest.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    summary = run_backtest(args.input, args.output)
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
