from typing import Dict
import json
from pathlib import Path


class EligibilityEngine:
    """
    Applies hard constraints to determine
    whether a stock is eligible for recommendation.
    """

    def __init__(self, rules_path: str):
        self.rules = self._load_rules(rules_path)

    def evaluate(self, context: Dict) -> Dict:

        blocking_reasons = []
        warnings = []

        # 1️⃣ Fundamental check
        if not context["fundamental"]["approved"]:
            blocking_reasons.append("FUNDAMENTAL_REJECTED")

        # 2️⃣ Liquidity check
        if not context["liquidity"]["tradable"]:
            blocking_reasons.append("NOT_TRADABLE")

        # 3️⃣ Setup existence
        if not context["setups"]:
            blocking_reasons.append("NO_VALID_SETUP")

        # 4️⃣ Position state
        if context.get("position_state") == "OPEN":
            blocking_reasons.append("OPEN_POSITION_EXISTS")

        # 5️⃣ Market regime constraint
        market_regime = context["market_regime"]["regime"]

        if (
            market_regime == "BEARISH"
            and self.rules["block_in_bearish_market"]
        ):
            blocking_reasons.append("MARKET_BEARISH")

        # 6️⃣ Trend requirement
        if (
            self.rules["require_uptrend_for_long"]
            and context["trend"]["trend"] != "UP"
        ):
            blocking_reasons.append("NOT_IN_UPTREND")

        # 7️⃣ Sector warning or block
        sector_strength = context["sector_strength"]["strength"]

        if sector_strength == "WEAK":
            if self.rules["block_if_sector_weak"]:
                blocking_reasons.append("WEAK_SECTOR")
            else:
                warnings.append("SECTOR_WEAK")

        return {
            "eligible": len(blocking_reasons) == 0,
            "blocking_reasons": blocking_reasons,
            "warnings": warnings
        }

    @staticmethod
    def _load_rules(path: str) -> Dict:
        with open(Path(path), "r", encoding="utf-8") as f:
            return json.load(f)
