from typing import Dict
import json
from pathlib import Path
import pandas as pd


class SectorStrengthAnalyzer:
    """
    Analyzes relative strength of sectors vs market index.
    """

    def __init__(self, rules_path: str):
        self.rules = self._load_rules(rules_path)

    def analyze(
        self,
        sector_data: Dict[str, pd.DataFrame],
        index_df: pd.DataFrame
    ) -> Dict[str, Dict]:

        results = {}

        index_return = self._calculate_return(
            index_df,
            self.rules["lookback_days"]
        )

        for sector, df in sector_data.items():
            sector_return = self._calculate_return(
                df,
                self.rules["lookback_days"]
            )

            relative_return = sector_return - index_return
            trend = self._detect_trend(df)
            strength = self._classify_strength(relative_return, trend)

            results[sector] = {
                "strength": strength,
                "relative_return": round(relative_return, 2),
                "trend": trend
            }

        return results

    # -----------------------------
    # Internal helpers
    # -----------------------------

    def _calculate_return(self, df: pd.DataFrame, days: int) -> float:
        if len(df) < days:
            return 0.0

        start_price = df.iloc[-days]["close"]
        end_price = df.iloc[-1]["close"]

        return ((end_price - start_price) / start_price) * 100

    def _detect_trend(self, df: pd.DataFrame) -> str:
        latest = df.iloc[-1]

        price = latest["close"]
        ema_50 = latest.get("ema_50")
        ema_200 = latest.get("ema_200")

        if price > ema_50 > ema_200:
            return "UP"
        elif price < ema_50 < ema_200:
            return "DOWN"
        else:
            return "SIDEWAYS"

    def _classify_strength(self, rel_return: float, trend: str) -> str:
        if rel_return >= self.rules["strong_threshold"] and trend == "UP":
            return "STRONG"

        if rel_return <= self.rules["weak_threshold"] and trend == "DOWN":
            return "WEAK"

        return "NEUTRAL"

    @staticmethod
    def _load_rules(path: str) -> Dict:
        with open(Path(path), "r", encoding="utf-8") as f:
            return json.load(f)
