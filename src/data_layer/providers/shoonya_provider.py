import pandas as pd
from typing import List, Dict
from .base_provider import MarketDataProvider


class ShoonyaProvider(MarketDataProvider):

    def __init__(self, client):
        self.client = client

    def fetch_ohlcv(
        self,
        symbols: List[str],
        lookback_days: int
    ) -> Dict[str, pd.DataFrame]:

        data = {}

        for symbol in symbols:
            candles = self.client.get_time_price_series(
                exchange="NSE",
                symbol=symbol,
                interval="1d",
                days=lookback_days
            )

            if not candles:
                continue

            df = pd.DataFrame(candles)
            df = df.rename(columns={
                "time": "date",
                "into": "open",
                "inth": "high",
                "intl": "low",
                "intc": "close",
                "intv": "volume"
            })

            df["date"] = pd.to_datetime(df["date"])
            df = df[["date", "open", "high", "low", "close", "volume"]]

            data[symbol] = df

        return data
