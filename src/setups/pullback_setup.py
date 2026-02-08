from typing import Dict, Optional
import pandas as pd
from .base_setup import SetupDetector


class PullbackSetup(SetupDetector):

    def detect(
        self,
        df: pd.DataFrame,
        trend_info: Dict
    ) -> Optional[Dict]:

        if trend_info["trend"] != "UP":
            return None

        latest = df.iloc[-1]

        near_ema = (
            abs(latest["close"] - latest["ema_20"]) / latest["ema_20"] < 0.01
            or abs(latest["close"] - latest["ema_50"]) / latest["ema_50"] < 0.015
        )

        volume_contraction = latest["volume"] < latest["vol_avg_20"]
        rsi_ok = 40 <= latest["rsi_14"] <= 55

        if near_ema and volume_contraction and rsi_ok:
            return {
                "setup_type": "PULLBACK",
                "triggered_on": str(latest["date"]),
                "strength": "MEDIUM",
                "evidence": {
                    "price": round(latest["close"], 2),
                    "ema_20": round(latest["ema_20"], 2),
                    "ema_50": round(latest["ema_50"], 2),
                    "rsi": round(latest["rsi_14"], 1)
                }
            }

        return None
