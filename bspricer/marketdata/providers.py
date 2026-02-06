from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd


@dataclass
class CsvMarketDataProvider:
    root: Path

    def load_spot_series(self, symbol: str) -> pd.Series:
        path = self.root / f"{symbol}_spot.csv"
        df = pd.read_csv(path, parse_dates=[0])
        df.columns = ["date", "spot"]
        return df.set_index("date")["spot"]

    def load_yield_curve(self, curve_name: str) -> pd.DataFrame:
        path = self.root / f"{curve_name}_curve.csv"
        df = pd.read_csv(path)
        df.columns = ["tenor", "rate"]
        return df
