from dataclasses import dataclass
from typing import List
from pathlib import Path
import csv


@dataclass(frozen=True)
class StockUniverseItem:
    symbol: str
    exchange: str
    sector: str


class StockUniverse:
    def __init__(self, stocks: List[StockUniverseItem]):
        self._stocks = stocks

    @property
    def stocks(self) -> List[StockUniverseItem]:
        return self._stocks

    @property
    def symbols(self) -> List[str]:
        return [s.symbol for s in self._stocks]

    @property
    def sectors(self) -> List[str]:
        return sorted({s.sector for s in self._stocks})


class StockUniverseLoader:
    REQUIRED_COLUMNS = {"symbol", "exchange", "sector", "enabled"}

    def __init__(self, csv_file: str):
        self.csv_file = Path(csv_file)

    def load(self) -> StockUniverse:
        if not self.csv_file.exists():
            raise FileNotFoundError(
                f"Universe CSV not found: {self.csv_file}"
            )

        stocks: List[StockUniverseItem] = []

        with open(self.csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            self._validate_header(reader.fieldnames)

            for row in reader:
                if not self._is_enabled(row):
                    continue

                stocks.append(
                    StockUniverseItem(
                        symbol=row["symbol"].strip().upper(),
                        exchange=row["exchange"].strip().upper(),
                        sector=row["sector"].strip().upper()
                    )
                )

        if not stocks:
            raise ValueError("No enabled stocks found in universe CSV")

        return StockUniverse(stocks=stocks)

    def _validate_header(self, headers):
        if headers is None:
            raise ValueError("Universe CSV has no header row")

        missing = self.REQUIRED_COLUMNS - set(h.lower() for h in headers)
        if missing:
            raise ValueError(
                f"Universe CSV missing columns: {missing}"
            )

    def _is_enabled(self, row: dict) -> bool:
        return row.get("enabled", "0").strip() in {"1", "true", "TRUE", "yes", "YES"}
