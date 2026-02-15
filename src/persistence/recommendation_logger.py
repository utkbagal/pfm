import json
from pathlib import Path
from typing import Dict


class RecommendationLogger:
    """
    Persists recommendation evidence to storage.
    """

    def __init__(self, base_path: str = "recommendation_logs"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    def log(self, evidence: Dict):

        symbol = evidence["symbol"]
        timestamp = evidence["run_timestamp"]

        filename = f"{symbol}_{timestamp}.json"
        file_path = self.base_path / filename

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=4)
