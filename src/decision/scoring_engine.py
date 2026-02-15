from typing import Dict
import json
from pathlib import Path


class ScoringEngine:
    """
    Assigns weighted score to eligible stocks.
    """

    def __init__(self, weights_path: str):
        self.weights = self._load_weights(weights_path)

    def score(self, context: Dict) -> Dict:

        breakdown = {}

        breakdown["setup"] = self._score_setup(context["setups"])
        breakdown["trend"] = self._score_trend(context["trend"])
        breakdown["volume"] = self._score_volume(context["setups"])
        breakdown["sector"] = self._score_sector(context["sector_strength"])
        breakdown["market"] = self._score_market(context["market_regime"])
        breakdown["relative_strength"] = self._score_relative_strength(
            context.get("relative_strength", 0)
        )

        total_score = sum(breakdown.values())

        return {
            "score": round(total_score),
            "breakdown": breakdown
        }

    # -----------------------------
    # Component scoring methods
    # -----------------------------

    def _score_setup(self, setups):
        if not setups:
            return 0

        setup_weight = self.weights["setup"]

        best_strength = max(
            (s["strength"] for s in setups),
            default="LOW"
        )

        strength_map = {
            "HIGH": 1.0,
            "MEDIUM": 0.7,
            "LOW": 0.4
        }

        return setup_weight * strength_map.get(best_strength, 0)

    def _score_trend(self, trend_info):
        weight = self.weights["trend"]

        if trend_info["trend"] == "UP":
            if trend_info["strength"] == "STRONG":
                return weight
            return weight * 0.7

        return weight * 0.2

    def _score_volume(self, setups):
        weight = self.weights["volume"]

        if not setups:
            return 0

        for s in setups:
            if "volume_multiple" in s["evidence"]:
                vol_mult = s["evidence"]["volume_multiple"]
                if vol_mult >= 1.7:
                    return weight
                elif vol_mult >= 1.3:
                    return weight * 0.7

        return weight * 0.4

    def _score_sector(self, sector_info):
        weight = self.weights["sector"]

        strength = sector_info["strength"]

        if strength == "STRONG":
            return weight
        if strength == "NEUTRAL":
            return weight * 0.6
        return weight * 0.2

    def _score_market(self, market_info):
        weight = self.weights["market"]

        regime = market_info["regime"]

        if regime == "BULLISH":
            return weight
        if regime == "NEUTRAL":
            return weight * 0.6
        return weight * 0.2

    def _score_relative_strength(self, rs_percent):
        weight = self.weights["relative_strength"]

        if rs_percent >= 5:
            return weight
        if rs_percent >= 2:
            return weight * 0.7
        if rs_percent >= 0:
            return weight * 0.4
        return weight * 0.1

    @staticmethod
    def _load_weights(path: str):
        with open(Path(path), "r", encoding="utf-8") as f:
            return json.load(f)
