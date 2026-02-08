import yfinance as yf
import pandas as pd
from typing import List, Dict
from .base_provider import MarketDataProvider


class YahooFinanceProvider(MarketDataProvider):

    def __init__(self, interval="1d", exchange_suffix=".NS"):
        self.interval = interval
        self.exchange_suffix = exchange_suffix

    def fetch_ohlcv(
        self,
        symbols: List[str],
        lookback_days: int
    ) -> Dict[str, pd.DataFrame]:

        data = {}
        period = f"{lookback_days}d"

        for symbol in symbols:
            ticker = yf.Ticker(f"{symbol}{self.exchange_suffix}")
            df = ticker.history(period=period, interval=self.interval)

            if df.empty:
                continue

            df = (
                df.reset_index()
                  .rename(columns={
                      "Date": "date",
                      "Open": "open",
                      "High": "high",
                      "Low": "low",
                      "Close": "close",
                      "Volume": "volume"
                  })
            )

            df = df[["date", "open", "high", "low", "close", "volume"]]
            data[symbol] = df

        return data
