from typing import Dict, Optional
from .base_setup import SetupDetector
from .volume_analyzer import VolumeAnalyzer


class RSIReversalSetup(SetupDetector):

    def detect(self, df, trend_info: Dict) -> Optional[Dict]:

        if len(df) < 2:
            return None

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        rsi_cross = prev["rsi_14"] < 40 and latest["rsi_14"] > 40
        price_ok = latest["close"] > latest["ema_50"]
        volume_confirm = VolumeAnalyzer.is_volume_spike(df, threshold=1.3)

        if rsi_cross and price_ok and volume_confirm:
            return {
                "setup_type": "RSI_REVERSAL",
                "triggered_on": str(latest["date"]),
                "strength": "MEDIUM",
                "evidence": {
                    "prev_rsi": round(prev["rsi_14"], 1),
                    "current_rsi": round(latest["rsi_14"], 1),
                    "volume_multiple": round(
                        VolumeAnalyzer.volume_multiple(df), 2
                    )
                }
            }

        return None
