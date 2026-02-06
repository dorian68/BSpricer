from dataclasses import dataclass


@dataclass(frozen=True)
class CreditDefaultSwap:
    notional: float
    spread: float
    maturity: float
    payment_frequency: int = 4
    hazard_rate: float = 0.02
    recovery_rate: float = 0.4
    discount_rate: float = 0.02
