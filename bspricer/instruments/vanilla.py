from dataclasses import dataclass
from enum import Enum


class OptionType(str, Enum):
    CALL = "call"
    PUT = "put"


@dataclass(frozen=True)
class EquityOption:
    spot: float
    strike: float
    maturity: float
    rate: float
    dividend_yield: float
    vol: float
    option_type: OptionType = OptionType.CALL


@dataclass(frozen=True)
class FXOption:
    spot: float
    strike: float
    maturity: float
    domestic_rate: float
    foreign_rate: float
    vol: float
    option_type: OptionType = OptionType.CALL


@dataclass(frozen=True)
class RateOption:
    forward: float
    strike: float
    maturity: float
    discount_rate: float
    vol: float
    option_type: OptionType = OptionType.CALL
