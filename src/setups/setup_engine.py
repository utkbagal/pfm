from typing import List, Dict
import pandas as pd

from .breakout_setup import BreakoutSetup
from .pullback_setup import PullbackSetup
from .rsi_reversal_setup import RSIReversalSetup


class SetupDetectionEngine:
    """
    Runs multiple setup detectors on a stock.
    """

    def __init__(self):
        self.detectors = [
            BreakoutSetup(),
            PullbackSetup(),
            RSIReversalSetup()
        ]

    def detect_setups(
        self,
        df: pd.DataFrame,
        trend_info: Dict
    ) -> List[Dict]:

        setups = []

        for detector in self.detectors:
            result = detector.detect(df, trend_info)
            if result:
                setups.append(result)

        return setups
