from dataclasses import dataclass
from enum import Enum
from .vanilla import OptionType


class BarrierType(str, Enum):
    UP_AND_OUT = "up-and-out"
    DOWN_AND_OUT = "down-and-out"
    UP_AND_IN = "up-and-in"
    DOWN_AND_IN = "down-and-in"


@dataclass(frozen=True)
class BarrierOption:
    spot: float
    strike: float
    maturity: float
    rate: float
    dividend_yield: float
    vol: float
    barrier: float
    barrier_type: BarrierType
    option_type: OptionType = OptionType.CALL


@dataclass(frozen=True)
class AsianOption:
    spot: float
    strike: float
    maturity: float
    rate: float
    dividend_yield: float
    vol: float
    option_type: OptionType = OptionType.CALL


@dataclass(frozen=True)
class DigitalOption:
    spot: float
    strike: float
    maturity: float
    rate: float
    dividend_yield: float
    vol: float
    payout: float = 1.0
    option_type: OptionType = OptionType.CALL
