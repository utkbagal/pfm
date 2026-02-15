import pandas as pd


class VolumeAnalyzer:
    """
    Provides volume-based utilities for setup detection.
    """

    @staticmethod
    def volume_multiple(df: pd.DataFrame) -> float:
        latest = df.iloc[-1]
        avg_vol = latest.get("vol_avg_20", 0)
        if avg_vol == 0:
            return 0
        return latest["volume"] / avg_vol

    @staticmethod
    def is_volume_spike(df: pd.DataFrame, threshold: float = 1.5) -> bool:
        return VolumeAnalyzer.volume_multiple(df) >= threshold

    @staticmethod
    def is_volume_contraction(df: pd.DataFrame) -> bool:
        latest = df.iloc[-1]
        return latest["volume"] < latest.get("vol_avg_20", 0)

    @staticmethod
    def volume_trend_increasing(df: pd.DataFrame, lookback: int = 3) -> bool:
        recent = df["volume"].tail(lookback)
        return all(x < y for x, y in zip(recent, recent[1:]))
