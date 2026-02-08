from typing import Dict, List
import json
from pathlib import Path
import pandas as pd


class LiquidityVolatilityFilter:
    """
    Checks whether a stock is tradeable based on
    liquidity and volatility criteria.
    """

    def __init__(self, rules_path: str):
        self.rules = self._load_rules(rules_path)

    def evaluate(
        self,
        indicator_data: Dict[str, pd.DataFrame]
    ) -> Dict[str, Dict]:

        results = {}

        for symbol, df in indicator_data.items():
            failed = self._run_checks(df)

            results[symbol] = {
                "tradable": len(failed) == 0,
                "failed_checks": failed
            }

        return results

    # -----------------------------
    # Internal checks
    # -----------------------------

    def _run_checks(self, df: pd.DataFrame) -> List[str]:
        failed = []

        latest = df.iloc[-1]

        # 1️⃣ Liquidity check
        avg_vol = latest.get("vol_avg_20", 0)
        if avg_vol < self.rules["min_avg_volume"]:
            failed.append("LOW_LIQUIDITY")

        # 2️⃣ Volatility check (ATR %)
        atr = latest.get("atr_14", 0)
        close = latest.get("close", 1)

        atr_percent = (atr / close) * 100 if close else 0
        if atr_percent < self.rules["min_atr_percent"]:
            failed.append("LOW_VOLATILITY")

        # 3️⃣ Spread check (optional / placeholder)
        # This can be implemented later using L1 data

        return failed

    @staticmethod
    def _load_rules(path: str) -> Dict:
        with open(Path(path), "r", encoding="utf-8") as f:
            return json.load(f)
