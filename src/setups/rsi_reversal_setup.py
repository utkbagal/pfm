from typing import Dict, Optional
import pandas as pd
from .base_setup import SetupDetector


class RSIReversalSetup(SetupDetector):

    def detect(
        self,
        df: pd.DataFrame,
        trend_info: Dict
    ) -> Optional[Dict]:

        if len(df) < 2:
            return None

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        rsi_reversal = prev["rsi_14"] < 40 and latest["rsi_14"] > 40
        price_ok = latest["close"] > latest["ema_50"]

        if rsi_reversal and price_ok:
            return {
                "setup_type": "RSI_REVERSAL",
                "triggered_on": str(latest["date"]),
                "strength": "MEDIUM",
                "evidence": {
                    "prev_rsi": round(prev["rsi_14"], 1),
                    "current_rsi": round(latest["rsi_14"], 1),
                    "price": round(latest["close"], 2)
                }
            }

        return None
