from typing import Dict
import json
from pathlib import Path
import pandas as pd


class MarketRegimeAnalyzer:
    """
    Determines overall market regime:
    BULLISH / NEUTRAL / BEARISH
    """

    def __init__(self, rules_path: str):
        self.rules = self._load_rules(rules_path)

    def analyze(self, index_df: pd.DataFrame) -> Dict:
        latest = index_df.iloc[-1]

        price = latest["close"]
        ema_20 = latest.get("ema_20")
        ema_50 = latest.get("ema_50")
        ema_200 = latest.get("ema_200")
        atr = latest.get("atr_14")

        regime = "NEUTRAL"
        confidence = 0.5

        # -------- Trend logic --------
        bullish_conditions = [
            price > ema_50,
            ema_20 > ema_50 > ema_200
        ]

        bearish_conditions = [
            price < ema_50,
            ema_50 < ema_200
        ]

        if all(bullish_conditions):
            regime = "BULLISH"
            confidence = 0.8

        elif all(bearish_conditions):
            regime = "BEARISH"
            confidence = 0.8

        # -------- Volatility context --------
        atr_percent = (atr / price) * 100 if price else 0

        if atr_percent > self.rules["volatility"]["atr_percent_high"]:
            vol_state = "HIGH"
            confidence -= 0.1
        elif atr_percent < self.rules["volatility"]["atr_percent_low"]:
            vol_state = "LOW"
            confidence -= 0.1
        else:
            vol_state = "NORMAL"

        confidence = max(0.0, min(confidence, 1.0))

        return {
            "regime": regime,
            "confidence": round(confidence, 2),
            "signals": {
                "trend": "UP" if regime == "BULLISH" else
                         "DOWN" if regime == "BEARISH" else "SIDEWAYS",
                "volatility": vol_state
            }
        }

    @staticmethod
    def _load_rules(path: str) -> Dict:
        with open(Path(path), "r", encoding="utf-8") as f:
            return json.load(f)
