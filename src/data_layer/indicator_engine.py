import pandas as pd
import numpy as np
from typing import Dict


class IndicatorEngine:
    """
    Computes technical indicators on OHLCV data.
    """

    def __init__(
        self,
        ema_periods=(20, 50, 200),
        rsi_period=14,
        atr_period=14,
        bb_period=20,
        bb_std=2,
        vol_avg_period=20
    ):
        self.ema_periods = ema_periods
        self.rsi_period = rsi_period
        self.atr_period = atr_period
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.vol_avg_period = vol_avg_period

    def compute(
        self,
        ohlcv_data: Dict[str, pd.DataFrame]
    ) -> Dict[str, pd.DataFrame]:

        enriched = {}

        for symbol, df in ohlcv_data.items():
            df = df.copy()
            df.sort_values("date", inplace=True)

            self._add_ema(df)
            self._add_rsi(df)
            self._add_atr(df)
            self._add_bollinger_bands(df)
            self._add_volume_avg(df)

            enriched[symbol] = df

        return enriched

    # -------------------------------
    # Indicator implementations
    # -------------------------------

    def _add_ema(self, df: pd.DataFrame):
        for period in self.ema_periods:
            df[f"ema_{period}"] = (
                df["close"]
                .ewm(span=period, adjust=False)
                .mean()
            )

    def _add_rsi(self, df: pd.DataFrame):
        delta = df["close"].diff()

        gain = np.where(delta > 0, delta, 0.0)
        loss = np.where(delta < 0, -delta, 0.0)

        gain_ema = pd.Series(gain).ewm(
            span=self.rsi_period, adjust=False
        ).mean()

        loss_ema = pd.Series(loss).ewm(
            span=self.rsi_period, adjust=False
        ).mean()

        rs = gain_ema / loss_ema
        df["rsi_14"] = 100 - (100 / (1 + rs))

    def _add_atr(self, df: pd.DataFrame):
        high = df["high"]
        low = df["low"]
        close = df["close"]

        prev_close = close.shift(1)

        tr = pd.concat(
            [
                high - low,
                (high - prev_close).abs(),
                (low - prev_close).abs(),
            ],
            axis=1,
        ).max(axis=1)

        df["atr_14"] = tr.ewm(
            span=self.atr_period, adjust=False
        ).mean()

    def _add_bollinger_bands(self, df: pd.DataFrame):
        mid = df["close"].rolling(self.bb_period).mean()
        std = df["close"].rolling(self.bb_period).std()

        df["bb_middle"] = mid
        df["bb_upper"] = mid + self.bb_std * std
        df["bb_lower"] = mid - self.bb_std * std

    def _add_volume_avg(self, df: pd.DataFrame):
        df["vol_avg_20"] = (
            df["volume"]
            .rolling(self.vol_avg_period)
            .mean()
        )
