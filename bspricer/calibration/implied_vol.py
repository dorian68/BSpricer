from __future__ import annotations

from bspricer.models.black_scholes import price as bs_price, greeks as bs_greeks


def implied_vol_newton(
    target_price: float,
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    option_type: str = "call",
    tol: float = 1e-6,
    max_iter: int = 100,
) -> float:
    vol = 0.2
    for _ in range(max_iter):
        price = bs_price(spot, strike, maturity, rate, dividend_yield, vol, option_type)
        diff = price - target_price
        if abs(diff) < tol:
            return max(vol, 1e-6)
        vega = bs_greeks(spot, strike, maturity, rate, dividend_yield, vol, option_type)["vega"]
        if vega < 1e-8:
            break
        vol -= diff / vega
        if vol <= 0.0:
            vol = 1e-6
    return max(vol, 1e-6)
