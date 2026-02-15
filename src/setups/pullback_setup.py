from typing import Dict, Optional
from .base_setup import SetupDetector
from .volume_analyzer import VolumeAnalyzer


class PullbackSetup(SetupDetector):

    def detect(self, df, trend_info: Dict) -> Optional[Dict]:

        if trend_info["trend"] != "UP":
            return None

        if len(df) < 3:
            return None

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        near_ema = (
            abs(latest["close"] - latest["ema_20"]) / latest["ema_20"] < 0.01
            or abs(latest["close"] - latest["ema_50"]) / latest["ema_50"] < 0.015
        )

        volume_dry = VolumeAnalyzer.is_volume_contraction(df)
        rsi_recovering = latest["rsi_14"] > prev["rsi_14"]

        if near_ema and volume_dry and rsi_recovering:
            return {
                "setup_type": "PULLBACK",
                "triggered_on": str(latest["date"]),
                "strength": "MEDIUM",
                "evidence": {
                    "price": round(latest["close"], 2),
                    "rsi": round(latest["rsi_14"], 1),
                    "volume_multiple": round(
                        VolumeAnalyzer.volume_multiple(df), 2
                    )
                }
            }

        return None
