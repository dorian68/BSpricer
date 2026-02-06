import math
from dataclasses import dataclass


@dataclass(frozen=True)
class FlatCurve:
    rate: float

    def discount_factor(self, t: float) -> float:
        return math.exp(-self.rate * t)
