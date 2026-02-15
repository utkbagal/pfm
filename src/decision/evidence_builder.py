from datetime import datetime
from typing import Dict


class EvidenceBuilder:
    """
    Builds structured recommendation evidence snapshot.
    """

    def build(self, context: Dict) -> Dict:

        return {
            "symbol": context["symbol"],
            "run_timestamp": datetime.utcnow().isoformat(),

            "market_context": context["market_regime"],
            "sector_context": context["sector_strength"],

            "fundamental_status": context["fundamental"],
            "liquidity_status": context["liquidity"],

            "trend_analysis": context["trend"],
            "detected_setups": context["setups"],

            "score": context["score"],
            "buy_plan": context["buy_plan"]
        }
