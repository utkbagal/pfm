from typing import Dict, Optional
import pandas as pd
from .base_setup import SetupDetector
from .volume_analyzer import VolumeAnalyzer


class BreakoutSetup(SetupDetector):

    def detect(
        self,
        df: pd.DataFrame,
        trend_info: Dict
    ) -> Optional[Dict]:

        if trend_info["trend"] != "UP":
            return None

        if len(df) < 25:
            return None

        latest = df.iloc[-1]
        prev = df.iloc[:-1]

        range_high = prev["high"].tail(20).max()
        breakout_margin = (latest["close"] - range_high) / range_high

        volume_ok = VolumeAnalyzer.is_volume_spike(df, threshold=1.7)

        if (
            breakout_margin > 0.003
            and volume_ok
            and latest["rsi_14"] >= 60
        ):
            return {
                "setup_type": "BREAKOUT",
                "triggered_on": str(latest["date"]),
                "strength": "HIGH",
                "evidence": {
                    "range_high": round(range_high, 2),
                    "breakout_margin_pct": round(breakout_margin * 100, 2),
                    "volume_multiple": round(
                        VolumeAnalyzer.volume_multiple(df), 2
                    ),
                    "rsi": round(latest["rsi_14"], 1)
                }
            }

        return None
