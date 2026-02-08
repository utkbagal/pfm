from typing import Dict
import json
from pathlib import Path
import pandas as pd


class TrendAnalyzer:
    """
    Determines stock-level trend state.
    """

    def __init__(self, rules_path: str):
        self.rules = self._load_rules(rules_path)

    def analyze(self, df: pd.DataFrame) -> Dict:
        latest = df.iloc[-1]

        price = latest["close"]
        ema_20 = latest.get("ema_20")
        ema_50 = latest.get("ema_50")
        ema_200 = latest.get("ema_200")
        rsi = latest.get("rsi_14")

        ema_up = ema_20 > ema_50 > ema_200
        ema_down = ema_20 < ema_50 < ema_200

        # -------- Trend direction --------
        if ema_up and price > ema_50:
            trend = "UP"
        elif ema_down and price < ema_50:
            trend = "DOWN"
        else:
            trend = "RANGE"

        # -------- Strength assessment --------
        strength = "NEUTRAL"

        if trend == "UP" and rsi >= self.rules["rsi_trend_confirm_max"]:
            strength = "STRONG"
        elif trend == "DOWN" and rsi <= self.rules["rsi_trend_confirm_min"]:
            strength = "STRONG"
        elif trend == "RANGE":
            strength = "WEAK"

        return {
            "trend": trend,
            "strength": strength,
            "details": {
                "ema_alignment": ema_up if trend == "UP" else ema_down if trend == "DOWN" else False,
                "price_position": (
                    "ABOVE_50" if price > ema_50 else
                    "BELOW_50" if price < ema_50 else
                    "AT_50"
                )
            }
        }

    @staticmethod
    def _load_rules(path: str) -> Dict:
        with open(Path(path), "r", encoding="utf-8") as f:
            return json.load(f)
