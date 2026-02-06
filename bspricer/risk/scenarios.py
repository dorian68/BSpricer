from __future__ import annotations

from dataclasses import replace
from bspricer.marketdata.curves import FlatCurve


def apply_parallel_shift(curve: FlatCurve, shift_bps: float) -> FlatCurve:
    return replace(curve, rate=curve.rate + shift_bps / 10000.0)
