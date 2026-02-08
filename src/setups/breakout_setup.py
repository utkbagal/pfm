import pandas as pd
from typing import Dict, Optional
from .base_setup import SetupDetector


class BreakoutSetup(SetupDetector):

    def detect(
        self,
        df: pd.DataFrame,
        trend_info: Dict
    ) -> Optional[Dict]:

        if trend_info["trend"] != "UP":
            return None

        latest = df.iloc[-1]
        prev = df.iloc[:-1]

        range_high = prev["high"].tail(20).max()
        volume_multiple = (
            latest["volume"] / latest["vol_avg_20"]
            if latest["vol_avg_20"] else 0
        )

        if (
            latest["close"] > range_high
            and volume_multiple >= 1.5
            and latest["rsi_14"] >= 55
        ):
            return {
                "setup_type": "BREAKOUT",
                "triggered_on": str(latest["date"]),
                "strength": "HIGH",
                "evidence": {
                    "range_high": round(range_high, 2),
                    "volume_multiple": round(volume_multiple, 2),
                    "rsi": round(latest["rsi_14"], 1)
                }
            }

        return None
