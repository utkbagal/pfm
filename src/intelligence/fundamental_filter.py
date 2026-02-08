from typing import Dict, List
import json
from pathlib import Path


class FundamentalFilter:
    """
    Applies fundamental quality checks.
    Acts as a SAFETY GATE.
    """

    def __init__(self, rules_path: str):
        self.rules = self._load_rules(rules_path)

    def evaluate(
        self,
        fundamental_data: Dict[str, Dict]
    ) -> Dict[str, Dict]:

        results = {}

        for symbol, metrics in fundamental_data.items():
            failed = self._run_checks(metrics)

            results[symbol] = {
                "approved": len(failed) == 0,
                "failed_checks": failed
            }

        return results

    # -----------------------------
    # Internal logic
    # -----------------------------

    def _run_checks(self, m: Dict) -> List[str]:
        failed = []

        if m.get("roe", 0) < self.rules["roe_min"]:
            failed.append("ROE_TOO_LOW")

        if m.get("roce", 0) < self.rules["roce_min"]:
            failed.append("ROCE_TOO_LOW")

        if m.get("debt_to_equity", 999) > self.rules["debt_to_equity_max"]:
            failed.append("HIGH_DEBT")

        if m.get("sales_growth_3y", 0) < self.rules["sales_growth_3y_min"]:
            failed.append("LOW_SALES_GROWTH")

        if m.get("profit_growth_3y", 0) < self.rules["profit_growth_3y_min"]:
            failed.append("LOW_PROFIT_GROWTH")

        if self.rules["operating_cash_flow_positive"]:
            if m.get("operating_cash_flow", 0) <= 0:
                failed.append("NEGATIVE_CASH_FLOW")

        return failed

    @staticmethod
    def _load_rules(path: str) -> Dict:
        with open(Path(path), "r", encoding="utf-8") as f:
            return json.load(f)
