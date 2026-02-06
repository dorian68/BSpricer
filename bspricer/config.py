from dataclasses import dataclass


@dataclass(frozen=True)
class MarketEnvironment:
    rate: float
    dividend_yield: float = 0.0
    foreign_rate: float = 0.0
