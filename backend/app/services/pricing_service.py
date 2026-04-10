"""
ML Dynamic Pricing Service — LightGBM surge prediction + rule-based fallback

Features:
- LightGBM model for demand-supply surge prediction
- Rule-based pricing engine as fallback
- Feature engineering pipeline
- Model training and persistence
- Real-time inference with confidence scoring

Based on BI_Tech_Stack_ML_Systems.md architecture:
- 17 features for surge prediction
- Output: surge multiplier 1.0-3.0
- Platform fee: 3-5%
- GST: 12% transport + 18% services
"""

import os
import json
import math
import joblib
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

MODELS_DIR = Path(__file__).parent.parent.parent / "models" / "pricing"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODELS_DIR / "surge_model.pkl"
FEATURE_CONFIG_PATH = MODELS_DIR / "feature_config.json"

VEHICLE_TYPE_ENCODE = {
    "LCV": 0,
    "ICV": 1,
    "HCV": 2,
    "Tipper": 3,
    "Tractor": 4,
    "Trailer": 5,
}

CITY_TIERS = {
    "mumbai": 1,
    "delhi": 1,
    "bangalore": 1,
    "chennai": 1,
    "hyderabad": 1,
    "kolkata": 1,
    "pune": 1,
    "ahmedabad": 1,
    "jaipur": 2,
    "lucknow": 2,
    "chandigarh": 2,
    "indore": 2,
    "nagpur": 2,
    "coimbatore": 2,
    "kochi": 2,
    "bhopal": 2,
    "visakhapatnam": 2,
    "surat": 2,
    "vadodara": 2,
    "madurai": 2,
}

FESTIVAL_DATES = {
    (1, 14): "makar_sankranti",
    (1, 26): "republic_day",
    (3, 14): "holi",
    (4, 14): "ambedkar_jayanti",
    (8, 15): "independence_day",
    (10, 2): "gandhi_jayanti",
    (10, 12): "dussehra",
    (11, 1): "diwali",
    (11, 15): "chhath_puja",
    (12, 25): "christmas",
}

FESTIVAL_WINDOWS = {
    "diwali": 7,
    "dussehra": 5,
    "holi": 3,
    "chhath_puja": 3,
    "makar_sankranti": 2,
    "christmas": 3,
    "republic_day": 2,
    "independence_day": 2,
    "gandhi_jayanti": 2,
    "ambedkar_jayanti": 2,
}

INDIA_DIESEL_PRICE_DEFAULT = 89.62

ROUTE_DIFFICULTY = {
    "mumbai-delhi": 0.3,
    "mumbai-bangalore": 0.45,
    "chennai-kolkata": 0.55,
    "delhi-kolkata": 0.4,
    "mumbai-chennai": 0.5,
    "bangalore-hyderabad": 0.25,
    "delhi-jaipur": 0.2,
    "pune-bangalore": 0.5,
    "hyderabad-chennai": 0.35,
    "kolkata-guwahati": 0.7,
    "delhi-lucknow": 0.25,
    "mumbai-ahmedabad": 0.35,
}


class FeatureEngineer:
    def __init__(self, config_path=None):
        self.config = self._load_config(config_path) if config_path else {}

    @staticmethod
    def _load_config(path):
        if Path(path).exists():
            with open(path) as f:
                return json.load(f)
        return {}

    @staticmethod
    def get_city_tier(city: str) -> int:
        return CITY_TIERS.get(city.lower().strip(), 3)

    @staticmethod
    def is_festival(date: datetime) -> bool:
        month_day = (date.month, date.day)
        for fest_date, fest_name in FESTIVAL_DATES.items():
            window = FESTIVAL_WINDOWS.get(fest_name, 3)
            for delta in range(-1, window):
                check = date - timedelta(days=date.day - fest_date[1])
                if (date.month, date.day) == fest_date:
                    return True
        return False

    @staticmethod
    def get_rds_score(origin: str, destination: str) -> float:
        key = f"{origin.lower()}-{destination.lower()}"
        reverse_key = f"{destination.lower()}-{origin.lower()}"
        if key in ROUTE_DIFFICULTY:
            return ROUTE_DIFFICULTY[key]
        if reverse_key in ROUTE_DIFFICULTY:
            return ROUTE_DIFFICULTY[reverse_key]
        return 0.5

    def engineer_features(self, input_data: dict) -> np.ndarray:
        demand = input_data.get("demand", 10)
        supply = input_data.get("supply", 5)
        demand_supply_ratio = demand / max(supply, 1)

        city_tier = self.get_city_tier(input_data.get("city", ""))
        is_remote = int(input_data.get("is_remote", False))
        is_hill = int(input_data.get("is_hill", False))

        dt = input_data.get("datetime", datetime.now())
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        hour = dt.hour
        day_of_week = dt.weekday()
        is_weekend = int(day_of_week >= 5)
        is_festival = int(input_data.get("is_festival", self.is_festival(dt)))

        distance_km = input_data.get("distance_km", 500)
        rds_score = input_data.get(
            "rds_score",
            self.get_rds_score(
                input_data.get("origin_city", ""),
                input_data.get("destination_city", ""),
            ),
        )
        congestion_level = input_data.get("congestion_level", 0.3)
        vehicle_type = VEHICLE_TYPE_ENCODE.get(
            input_data.get("vehicle_category", "HCV"), 2
        )
        vehicle_age = input_data.get("vehicle_age", 3)
        diesel_price = input_data.get("diesel_price", INDIA_DIESEL_PRICE_DEFAULT)
        customer_type = {"high_value": 2, "medium": 1, "low_value": 0}.get(
            input_data.get("customer_type", "medium"), 1
        )

        features = np.array(
            [
                [
                    demand,
                    supply,
                    demand_supply_ratio,
                    city_tier,
                    is_remote,
                    is_hill,
                    hour,
                    day_of_week,
                    is_weekend,
                    is_festival,
                    distance_km,
                    rds_score,
                    congestion_level,
                    vehicle_type,
                    vehicle_age,
                    diesel_price,
                    customer_type,
                ]
            ]
        )

        return features

    def get_feature_names(self) -> list:
        return [
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


class SurgePredictor:
    def __init__(self, model_path=None):
        self.model = None
        self.feature_eng = FeatureEngineer()
        self.model_path = Path(model_path) if model_path else MODEL_PATH
        self._load_model()

    def _load_model(self):
        if self.model_path.exists():
            try:
                self.model = joblib.load(self.model_path)
                logger.info(f"Loaded surge model from {self.model_path}")
            except Exception as e:
                logger.warning(f"Failed to load model: {e}. Using rule-based fallback.")
                self.model = None
        else:
            logger.info("No trained model found. Using rule-based fallback.")

    def predict(self, input_data: dict) -> dict:
        features = self.feature_eng.engineer_features(input_data)
        feature_names = self.feature_eng.get_feature_names()

        if self.model is not None:
            try:
                surge_multiplier = float(self.model.predict(features)[0])
                surge_multiplier = max(1.0, min(surge_multiplier, 3.0))
                model_used = "lightgbm"
                confidence = 0.85
            except Exception as e:
                logger.warning(f"Model prediction failed: {e}. Falling back to rules.")
                surge_multiplier, confidence = self._rule_based_surge(input_data)
                model_used = "rule_based"
        else:
            surge_multiplier, confidence = self._rule_based_surge(input_data)
            model_used = "rule_based"

        return {
            "surge_multiplier": round(surge_multiplier, 3),
            "confidence": round(confidence, 3),
            "model_used": model_used,
            "features": dict(zip(feature_names, features[0].tolist())),
        }

    def _rule_based_surge(self, data: dict) -> tuple:
        surge = 1.0
        confidence = 0.9

        demand = data.get("demand", 10)
        supply = data.get("supply", 5)
        ratio = demand / max(supply, 1)

        if ratio >= 4.0:
            surge += 0.6
        elif ratio >= 3.0:
            surge += 0.4
        elif ratio >= 2.0:
            surge += 0.2
        elif ratio >= 1.5:
            surge += 0.1

        if data.get("is_remote", False):
            surge += 0.25
        if data.get("is_hill", False):
            surge += 0.35
        if data.get("is_festival", False):
            surge += 0.3
        if data.get("congestion_level", 0.3) > 0.6:
            surge += 0.15

        dt = data.get("datetime", datetime.now())
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        if dt.hour >= 22 or dt.hour < 5:
            surge += 0.1
        if dt.weekday() >= 5:
            surge += 0.05

        surge = min(surge, 3.0)
        return surge, confidence


class DynamicPricingEngine:
    RATE_PER_KM = {
        "LCV": 12.0,
        "ICV": 15.0,
        "HCV": 18.0,
        "Tipper": 20.0,
        "Tractor": 16.0,
        "Trailer": 22.0,
    }

    CITY_TIER_MULTIPLIER = {1: 0.95, 2: 1.0, 3: 1.15}

    SURCHARGE_RANGES = {
        "festival": {"min": 20, "max": 60, "typical": 30},
        "remote": {"min": 25, "max": 50, "typical": 35},
        "hill": {"min": 35, "max": 60, "typical": 45},
        "congestion": {"min": 10, "max": 25, "typical": 15},
    }

    SERVICE_MULTIPLIERS = {"standard": 1.0, "express": 1.5, "priority": 1.8}

    def __init__(self, use_ml: bool = True):
        self.surge_predictor = SurgePredictor() if use_ml else None
        self.use_ml = use_ml

    def calculate_price(self, params: dict) -> dict:
        weight_kg = params["weight_kg"]
        distance_km = params["distance_km"]
        vehicle_category = params.get("vehicle_category", "HCV")
        is_interstate = params.get("is_interstate", False)
        is_festival = params.get("is_festival", False)
        is_remote = params.get("is_remote", False)
        is_hill = params.get("is_hill", False)
        is_congested = params.get("is_congested", False)
        origin_city = params.get("origin_city", "")
        destination_city = params.get("destination_city", "")
        service_type = params.get("service_type", "standard")
        customer_type = params.get("customer_type", "medium")
        demand = params.get("demand", 10)
        supply = params.get("supply", 5)

        base_rate = self.RATE_PER_KM.get(vehicle_category, 18.0)
        base_cost = distance_km * base_rate

        fe = FeatureEngineer()
        city_tier = fe.get_city_tier(origin_city if origin_city else destination_city)
        tier_mult = self.CITY_TIER_MULTIPLIER.get(city_tier, 1.15)

        fuel_index = 1.0
        diesel_price = params.get("diesel_price", INDIA_DIESEL_PRICE_DEFAULT)
        if diesel_price > 95:
            fuel_index = 1.05 + (diesel_price - 95) * 0.005
        elif diesel_price < 85:
            fuel_index = 0.98

        tier_adjusted_cost = base_cost * tier_mult * fuel_index

        surcharges = {}
        total_surcharge_pct = 0

        if is_festival:
            pct = self.SURCHARGE_RANGES["festival"]["typical"]
            surcharges["festival"] = pct
            total_surcharge_pct += pct
        if is_remote:
            pct = self.SURCHARGE_RANGES["remote"]["typical"]
            surcharges["remote"] = pct
            total_surcharge_pct += pct
        if is_hill:
            pct = self.SURCHARGE_RANGES["hill"]["typical"]
            surcharges["hill"] = pct
            total_surcharge_pct += pct
        if is_congested:
            pct = self.SURCHARGE_RANGES["congestion"]["typical"]
            surcharges["congestion"] = pct
            total_surcharge_pct += pct

        surcharge_amount = tier_adjusted_cost * (total_surcharge_pct / 100)

        surge_input = {
            "demand": demand,
            "supply": supply,
            "city": origin_city,
            "is_remote": is_remote,
            "is_hill": is_hill,
            "is_festival": is_festival,
            "distance_km": distance_km,
            "origin_city": origin_city,
            "destination_city": destination_city,
            "congestion_level": 0.5 if is_congested else 0.2,
            "vehicle_category": vehicle_category,
            "customer_type": customer_type,
        }

        if self.use_ml and self.surge_predictor:
            surge_result = self.surge_predictor.predict(surge_input)
            surge_mult = surge_result["surge_multiplier"]
            surge_model = surge_result["model_used"]
            surge_confidence = surge_result["confidence"]
        else:
            ratio = demand / max(supply, 1)
            if ratio >= 4:
                surge_mult = 1.6
            elif ratio >= 3:
                surge_mult = 1.4
            elif ratio >= 2:
                surge_mult = 1.2
            elif ratio >= 1.5:
                surge_mult = 1.1
            else:
                surge_mult = 1.0
            surge_model = "rule_based"
            surge_confidence = 0.9

        surge_amount = (tier_adjusted_cost + surcharge_amount) * (surge_mult - 1.0)

        service_mult = self.SERVICE_MULTIPLIERS.get(service_type, 1.0)
        service_amount = (tier_adjusted_cost + surcharge_amount + surge_amount) * (
            service_mult - 1.0
        )

        subtotal = tier_adjusted_cost + surcharge_amount + surge_amount + service_amount

        platform_fee_pct = 4.0 if distance_km > 200 else 5.0
        platform_fee = subtotal * (platform_fee_pct / 100)

        customer_discount = 0
        if customer_type == "high_value":
            customer_discount = subtotal * 0.10
        elif customer_type == "low_value":
            customer_discount = -subtotal * 0.05

        transport_gst = tier_adjusted_cost * 0.12
        service_gst = platform_fee * 0.18
        gst_amount = transport_gst + service_gst

        final_price = subtotal - customer_discount + platform_fee + gst_amount

        return {
            "base_cost": round(base_cost, 2),
            "base_rate_per_km": base_rate,
            "city_tier": city_tier,
            "tier_multiplier": tier_mult,
            "fuel_index": round(fuel_index, 4),
            "tier_adjusted_cost": round(tier_adjusted_cost, 2),
            "surcharges": surcharges,
            "total_surcharge_pct": total_surcharge_pct,
            "surcharge_amount": round(surcharge_amount, 2),
            "surge_multiplier": round(surge_mult, 3),
            "surge_model": surge_model,
            "surge_confidence": round(surge_confidence, 3),
            "surge_amount": round(surge_amount, 2),
            "service_type": service_type,
            "service_multiplier": service_mult,
            "service_amount": round(service_amount, 2),
            "subtotal": round(subtotal, 2),
            "customer_type": customer_type,
            "customer_adjustment": round(customer_discount, 2),
            "platform_fee_pct": platform_fee_pct,
            "platform_fee": round(platform_fee, 2),
            "gst_breakdown": {
                "transport_gst_12pct": round(transport_gst, 2),
                "service_gst_18pct": round(service_gst, 2),
            },
            "gst_amount": round(gst_amount, 2),
            "savings_vs_broker_pct": round(self._calc_savings(platform_fee_pct), 1),
            "final_price": round(final_price, 2),
            "currency": "INR",
            "breakdown_per_km": round(final_price / max(distance_km, 1), 2),
        }

    @staticmethod
    def _calc_savings(platform_fee_pct: float) -> float:
        broker_pct = 10.0
        savings = ((broker_pct - platform_fee_pct) / broker_pct) * 100
        return max(savings, 0)

    def get_rate_card(self) -> dict:
        return {
            "base_rates_per_km": self.RATE_PER_KM,
            "city_tier_multipliers": self.CITY_TIER_MULTIPLIER,
            "surcharge_ranges": self.SURCHARGE_RANGES,
            "service_multipliers": self.SERVICE_MULTIPLIERS,
            "platform_fee_pct": {"short_haul_lt_200km": 5.0, "long_haul_gt_200km": 4.0},
            "gst_rates": {"transport": 12, "services": 18},
            "demand_supply_surge": {
                "1:1": "1.0x (normal)",
                "2:1": "1.2x (+20%)",
                "3:1": "1.4x (+40%)",
                "4:1+": "1.6x (+60%, capped)",
            },
            "customer_discounts": {
                "high_value": "-10%",
                "medium": "0%",
                "low_value": "+5%",
            },
        }


pricing_engine = DynamicPricingEngine(use_ml=True)
