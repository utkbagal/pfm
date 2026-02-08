from abc import ABC, abstractmethod
from typing import Dict, Optional
import pandas as pd


class SetupDetector(ABC):

    @abstractmethod
    def detect(
        self,
        df: pd.DataFrame,
        trend_info: Dict
    ) -> Optional[Dict]:
        """
        Returns setup dict if detected, else None
        """
        pass
