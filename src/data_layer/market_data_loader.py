import json
from pathlib import Path
from typing import Dict

from .providers.yahoo_provider import YahooFinanceProvider
from .providers.shoonya_provider import ShoonyaProvider


class MarketDataLoader:

    def __init__(self, config_path: str, shoonya_client=None):
        self.config = self._load_config(config_path)
        self.provider_name = self.config["provider"]
        self.shoonya_client = shoonya_client

        self.provider = self._init_provider()

    def fetch(self, symbols, lookback_days=None) -> Dict:
        if lookback_days is None:
            lookback_days = self.config["defaults"]["lookback_days"]

        return self.provider.fetch_ohlcv(symbols, lookback_days)

    def _init_provider(self):
        if self.provider_name == "yahoo":
            yahoo_cfg = self.config.get("yahoo", {})
            return YahooFinanceProvider(
                interval=yahoo_cfg.get("interval", "1d"),
                exchange_suffix=yahoo_cfg.get("exchange_suffix", ".NS")
            )

        if self.provider_name == "shoonya":
            if not self.shoonya_client:
                raise ValueError("Shoonya client required for shoonya provider")
            return ShoonyaProvider(self.shoonya_client)

        raise ValueError(f"Unknown market data provider: {self.provider_name}")

    @staticmethod
    def _load_config(path: str) -> dict:
        with open(Path(path), "r", encoding="utf-8") as f:
            return json.load(f)
