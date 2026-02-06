from __future__ import annotations

from typing import Iterable

from bspricer.instruments.vanilla import RateOption
from bspricer.marketdata.curves import FlatCurve
from bspricer.models.black_76 import price as black_76_price


def price_rate_option(option: RateOption) -> float:
    return black_76_price(
        forward=option.forward,
        strike=option.strike,
        maturity=option.maturity,
        discount_rate=option.discount_rate,
        vol=option.vol,
        option_type=option.option_type.value,
    )


def price_zero_coupon(face: float, maturity: float, curve: FlatCurve) -> float:
    return face * curve.discount_factor(maturity)


def swap_annuity(curve: FlatCurve, payment_times: Iterable[float], accrual: float) -> float:
    return sum(curve.discount_factor(t) * accrual for t in payment_times)


def par_swap_rate(curve: FlatCurve, payment_times: Iterable[float], accrual: float) -> float:
    payment_times = list(payment_times)
    if not payment_times:
        return 0.0
    annuity = swap_annuity(curve, payment_times, accrual)
    if annuity <= 0.0:
        return 0.0
    return (1.0 - curve.discount_factor(payment_times[-1])) / annuity


def price_fixed_floating_swap(
    fixed_rate: float,
    notional: float,
    curve: FlatCurve,
    payment_times: Iterable[float],
    accrual: float,
) -> float:
    payment_times = list(payment_times)
    if not payment_times:
        return 0.0
    fixed_leg = fixed_rate * swap_annuity(curve, payment_times, accrual) * notional
    float_leg = notional * (1.0 - curve.discount_factor(payment_times[-1]))
    return float_leg - fixed_leg
