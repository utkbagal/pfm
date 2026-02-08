from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict


class MarketDataProvider(ABC):

    @abstractmethod
    def fetch_ohlcv(
        self,
        symbols: List[str],
        lookback_days: int
    ) -> Dict[str, pd.DataFrame]:
        """
        Returns:
        {
          "RELIANCE": DataFrame(date, open, high, low, close, volume),
          ...
        }
        """
        pass
