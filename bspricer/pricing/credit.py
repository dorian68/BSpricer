from __future__ import annotations

import math

from bspricer.instruments.credit import CreditDefaultSwap


def _payment_schedule(maturity: float, payment_frequency: int) -> tuple[list[float], float]:
    frequency = max(int(payment_frequency), 1)
    n_payments = max(int(round(maturity * frequency)), 1)
    dt = maturity / n_payments
    times = [dt * i for i in range(1, n_payments + 1)]
    return times, dt


def price_cds(cds: CreditDefaultSwap) -> float:
    times, dt = _payment_schedule(cds.maturity, cds.payment_frequency)
    premium_leg = 0.0
    protection_leg = 0.0
    prev_survival = 1.0
    for t in times:
        survival = math.exp(-cds.hazard_rate * t)
        df = math.exp(-cds.discount_rate * t)
        premium_leg += cds.spread * df * survival * dt
        protection_leg += (1.0 - cds.recovery_rate) * df * (prev_survival - survival)
        prev_survival = survival
    return cds.notional * (protection_leg - premium_leg)


def fair_cds_spread(cds: CreditDefaultSwap) -> float:
    times, dt = _payment_schedule(cds.maturity, cds.payment_frequency)
    premium_denom = 0.0
    protection_leg = 0.0
    prev_survival = 1.0
    for t in times:
        survival = math.exp(-cds.hazard_rate * t)
        df = math.exp(-cds.discount_rate * t)
        premium_denom += df * survival * dt
        protection_leg += (1.0 - cds.recovery_rate) * df * (prev_survival - survival)
        prev_survival = survival
    if premium_denom <= 0.0:
        return 0.0
    return protection_leg / premium_denom
