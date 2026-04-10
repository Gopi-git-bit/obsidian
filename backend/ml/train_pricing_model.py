"""
LightGBM Surge Pricing Model Training Pipeline

Generates synthetic Indian logistics data and trains a surge prediction model.
Features based on BI_Tech_Stack_ML_Systems.md (17 features).

Usage:
    python -m ml.train_pricing_model [--samples 50000] [--output models/pricing/]
"""

import argparse
import json
import math
import random
from pathlib import Path
from datetime import datetime, timedelta

import numpy as np


CITY_TIERS_DATA = {
    1: {
        "cities": [
            "mumbai",
            "delhi",
            "bangalore",
            "chennai",
            "hyderabad",
            "kolkata",
            "pune",
            "ahmedabad",
        ],
        "base_demand": (40, 100),
        "base_supply": (20, 60),
        "base_rate": (16, 25),
    },
    2: {
        "cities": [
            "jaipur",
            "lucknow",
            "chandigarh",
            "indore",
            "nagpur",
            "coimbatore",
            "kochi",
            "bhopal",
            "visakhapatnam",
            "surat",
            "vadodara",
            "madurai",
        ],
        "base_demand": (15, 50),
        "base_supply": (10, 35),
        "base_rate": (14, 22),
    },
    3: {
        "cities": [
            "varanasi",
            "allahabad",
            "ranchi",
            "durgapur",
            "bareilly",
            "moradabad",
            "apur",
            "tirunelveli",
            "gwalior",
            "udaipur",
            "siliguri",
            "solapur",
            "jalgaon",
            "guntur",
            "karnal",
            "panipat",
            "rohtak",
            "hissar",
        ],
        "base_demand": (5, 25),
        "base_supply": (3, 18),
        "base_rate": (12, 20),
    },
}

VEHICLE_CATEGORIES = {
    "LCV": {"payload": (500, 2500), "rate_per_km": (10, 18), "mileage": (12, 18)},
    "ICV": {"payload": (2500, 7000), "rate_per_km": (14, 22), "mileage": (8, 14)},
    "HCV": {"payload": (7000, 25000), "rate_per_km": (18, 30), "mileage": (4, 8)},
    "Tipper": {"payload": (5000, 20000), "rate_per_km": (16, 28), "mileage": (4, 7)},
}

POPULAR_CORRIDORS = [
    ("mumbai", "delhi", 1400),
    ("mumbai", "bangalore", 980),
    ("mumbai", "chennai", 1330),
    ("mumbai", "hyderabad", 710),
    ("mumbai", "ahmedabad", 530),
    ("mumbai", "pune", 150),
    ("delhi", "kolkata", 1460),
    ("delhi", "jaipur", 270),
    ("delhi", "lucknow", 550),
    ("delhi", "chandigarh", 250),
    ("delhi", "ahmedabad", 950),
    ("delhi", "hyderabad", 1590),
    ("chennai", "bangalore", 350),
    ("chennai", "hyderabad", 630),
    ("chennai", "kolkata", 1670),
    ("bangalore", "hyderabad", 570),
    ("bangalore", "kochi", 370),
    ("pune", "hyderabad", 560),
    ("ahmedabad", "jaipur", 600),
    ("kolkata", "guwahati", 1020),
    ("nagpur", "hyderabad", 500),
]

FESTIVAL_MONTHS = {10: 1.35, 11: 1.45, 3: 1.25, 1: 1.15, 12: 1.30, 7: 1.15, 8: 1.10}


def generate_synthetic_data(n_samples: int = 50000, seed: int = 42) -> list[dict]:
    random.seed(seed)
    np.random.seed(seed)

    samples = []
    for _ in range(n_samples):
        tier = random.choices([1, 2, 3], weights=[0.45, 0.35, 0.20])[0]
        tier_data = CITY_TIERS_DATA[tier]
        city = random.choice(tier_data["cities"])

        origin, destination, distance = random.choice(POPULAR_CORRIDORS)
        distance_variation = np.random.normal(1.0, 0.1)
        actual_distance = max(50, distance * max(0.7, distance_variation))

        demand = random.randint(*tier_data["base_demand"])
        supply = random.randint(*tier_data["base_supply"])

        if random.random() < 0.15:
            demand = int(demand * random.uniform(1.5, 3.0))
        if random.random() < 0.1:
            supply = int(supply * random.uniform(0.3, 0.5))

        hour = random.randint(0, 23)
        day_of_week = random.randint(0, 6)
        is_weekend = int(day_of_week >= 5)
        month = random.randint(1, 12)

        is_festival = random.random() < 0.2
        festival_multiplier = FESTIVAL_MONTHS.get(month, 1.0)
        if is_festival:
            festival_multiplier = max(festival_multiplier, 1.25)

        vehicle_cat = random.choice(list(VEHICLE_CATEGORIES.keys()))
        veh_data = VEHICLE_CATEGORIES[vehicle_cat]
        weight_kg = random.uniform(*veh_data["payload"])
        vehicle_age = random.randint(1, 12)

        is_remote = 1 if tier == 3 and random.random() < 0.35 else 0
        is_hill = 1 if random.random() < 0.10 else 0
        congestion_level = (
            random.uniform(0.1, 0.9) if tier == 1 else random.uniform(0.05, 0.5)
        )

        route_difficulty = 0.3 if distance < 300 else (0.5 if distance < 800 else 0.7)
        if is_hill:
            route_difficulty = min(route_difficulty + 0.2, 1.0)
        if is_remote:
            route_difficulty = min(route_difficulty + 0.15, 1.0)

        diesel_price = np.random.normal(89.62, 5.0)
        diesel_price = max(75, min(diesel_price, 110))

        customer_type_map = {"high_value": 2, "medium": 1, "low_value": 0}
        customer_type = random.choices(
            ["high_value", "medium", "low_value"], weights=[0.3, 0.5, 0.2]
        )[0]

        demand_supply_ratio = demand / max(supply, 1)

        base_rate = random.uniform(*veh_data["rate_per_km"])
        city_tier_mult = {1: 0.95, 2: 1.0, 3: 1.15}[tier]
        fuel_index = 1.0 + max(0, (diesel_price - 88) * 0.003)

        surge = 1.0
        if demand_supply_ratio >= 4.0:
            surge += 0.6
        elif demand_supply_ratio >= 3.0:
            surge += 0.4
        elif demand_supply_ratio >= 2.0:
            surge += 0.2
        elif demand_supply_ratio >= 1.5:
            surge += 0.1

        if is_remote:
            surge += 0.25
        if is_hill:
            surge += 0.35
        if is_festival:
            surge += random.uniform(0.2, 0.6)
        if congestion_level > 0.6:
            surge += 0.15
        if hour >= 22 or hour < 5:
            surge += 0.1
        if is_weekend:
            surge += 0.05

        surge *= festival_multiplier
        surge = max(1.0, min(surge, 3.0))

        noise = np.random.normal(0, 0.03)
        surge = max(1.0, min(surge + noise, 3.0))
        surge = round(surge, 4)

        sample = {
            "demand": demand,
            "supply": supply,
            "demand_supply_ratio": round(demand_supply_ratio, 4),
            "city_tier": tier,
            "is_remote": is_remote,
            "is_hill": is_hill,
            "hour": hour,
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "is_festival": is_festival,
            "distance_km": round(actual_distance, 2),
            "rds_score": round(route_difficulty, 4),
            "congestion_level": round(congestion_level, 4),
            "vehicle_type": {"LCV": 0, "ICV": 1, "HCV": 2, "Tipper": 3}[vehicle_cat],
            "vehicle_age": vehicle_age,
            "diesel_price": round(diesel_price, 2),
            "customer_type": customer_type_map[customer_type],
            "surge_multiplier": surge,
            "base_rate_per_km": round(base_rate, 2),
            "origin_city": origin,
            "destination_city": destination,
            "weight_kg": round(weight_kg, 2),
            "vehicle_category": vehicle_cat,
        }
        samples.append(sample)

    return samples


def train_model(samples: list[dict], output_dir: Path) -> dict:
    try:
        import lightgbm as lgb
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        import joblib
    except ImportError:
        print("ERROR: lightgbm and scikit-learn are required for training.")
        print("Install with: pip install lightgbm scikit-learn")
        return {"status": "error", "message": "Missing dependencies"}

    feature_cols = [
        "demand",
        "supply",
        "demand_supply_ratio",
        "city_tier",
        "is_remote",
        "is_hill",
        "hour",
        "day_of_week",
        "is_weekend",
        "is_festival",
        "distance_km",
        "rds_score",
        "congestion_level",
        "vehicle_type",
        "vehicle_age",
        "diesel_price",
        "customer_type",
    ]

    X = np.array([[s[col] for col in feature_cols] for s in samples])
    y = np.array([s["surge_multiplier"] for s in samples])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = lgb.LGBMRegressor(
        objective="regression",
        n_estimators=500,
        learning_rate=0.05,
        max_depth=8,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_samples=20,
        reg_alpha=0.1,
        reg_lambda=0.1,
        random_state=42,
        verbose=-1,
    )

    model.fit(
        X_train,
        y_train,
        eval_set=[(X_test, y_test)],
        eval_metric="rmse",
        callbacks=[
            lgb.early_stopping(stopping_rounds=50),
            lgb.log_evaluation(period=100),
        ],
    )

    y_pred = model.predict(X_test)
    y_pred_clipped = np.clip(y_pred, 1.0, 3.0)

    rmse = mean_squared_error(y_test, y_pred_clipped) ** 0.5
    mae = mean_absolute_error(y_test, y_pred_clipped)
    r2 = r2_score(y_test, y_pred_clipped)

    metrics = {
        "rmse": round(rmse, 4),
        "mae": round(mae, 4),
        "r2": round(r2, 4),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "n_features": len(feature_cols),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "surge_model.pkl"
    joblib.dump(model, model_path)

    feature_config = {
        "feature_names": feature_cols,
        "target": "surge_multiplier",
        "target_range": [1.0, 3.0],
        "categories": {
            "vehicle_type": {"LCV": 0, "ICV": 1, "HCV": 2, "Tipper": 3},
            "customer_type": {"low_value": 0, "medium": 1, "high_value": 2},
            "city_tier": {"metro": 1, "tier2": 2, "town": 3},
        },
        "hyperparameters": {
            "n_estimators": 500,
            "learning_rate": 0.05,
            "max_depth": 8,
            "num_leaves": 31,
        },
        "metrics": metrics,
        "trained_at": datetime.now().isoformat(),
    }

    config_path = output_dir / "feature_config.json"
    with open(config_path, "w") as f:
        json.dump(feature_config, f, indent=2)

    feature_imp = dict(zip(feature_cols, model.feature_importances_.tolist()))
    feature_imp_path = output_dir / "feature_importance.json"
    with open(feature_imp_path, "w") as f:
        json.dump(feature_imp, f, indent=2)

    print(f"\nModel Training Complete!")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  MAE:  {mae:.4f}")
    print(f"  R2:   {r2:.4f}")
    print(f"  Model saved to: {model_path}")
    print(f"  Config saved to: {config_path}")
    print(f"\n  Feature Importance:")
    for feat, imp in sorted(feature_imp.items(), key=lambda x: -x[1]):
        print(f"    {feat}: {imp}")

    return metrics


def main():
    parser = argparse.ArgumentParser(description="Train LightGBM Surge Pricing Model")
    parser.add_argument(
        "--samples", type=int, default=50000, help="Number of synthetic samples"
    )
    parser.add_argument("--output", type=str, default=None, help="Output directory")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    output_dir = (
        Path(args.output)
        if args.output
        else Path(__file__).parent / "models" / "pricing"
    )

    print(f"Generating {args.samples} synthetic samples...")
    samples = generate_synthetic_data(args.samples, args.seed)
    print(f"Generated {len(samples)} samples")

    data_path = output_dir / "training_data.json"
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(data_path, "w") as f:
        json.dump(samples[:100], f)
    print(f"Sample data saved to {data_path}")

    metrics = train_model(samples, output_dir)
    print(f"\nFinal metrics: {metrics}")


if __name__ == "__main__":
    main()
