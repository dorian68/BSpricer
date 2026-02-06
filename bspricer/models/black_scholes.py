import math
from typing import Dict


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)


def _d1_d2(spot: float, strike: float, maturity: float, rate: float, dividend_yield: float, vol: float) -> tuple[float, float]:
    if maturity <= 0.0 or vol <= 0.0:
        return 0.0, 0.0
    vsqrt = vol * math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (rate - dividend_yield + 0.5 * vol * vol) * maturity) / vsqrt
    d2 = d1 - vsqrt
    return d1, d2


def price(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    option_type: str = "call",
) -> float:
    d1, d2 = _d1_d2(spot, strike, maturity, rate, dividend_yield, vol)
    df_r = math.exp(-rate * maturity)
    df_q = math.exp(-dividend_yield * maturity)
    if option_type == "call":
        return spot * df_q * _norm_cdf(d1) - strike * df_r * _norm_cdf(d2)
    return strike * df_r * _norm_cdf(-d2) - spot * df_q * _norm_cdf(-d1)


def greeks(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    option_type: str = "call",
) -> Dict[str, float]:
    d1, d2 = _d1_d2(spot, strike, maturity, rate, dividend_yield, vol)
    df_r = math.exp(-rate * maturity)
    df_q = math.exp(-dividend_yield * maturity)
    pdf = _norm_pdf(d1)
    if option_type == "call":
        delta = df_q * _norm_cdf(d1)
        theta = (
            -(spot * df_q * pdf * vol) / (2.0 * math.sqrt(maturity))
            - rate * strike * df_r * _norm_cdf(d2)
            + dividend_yield * spot * df_q * _norm_cdf(d1)
        )
        rho = strike * maturity * df_r * _norm_cdf(d2)
    else:
        delta = df_q * (_norm_cdf(d1) - 1.0)
        theta = (
            -(spot * df_q * pdf * vol) / (2.0 * math.sqrt(maturity))
            + rate * strike * df_r * _norm_cdf(-d2)
            - dividend_yield * spot * df_q * _norm_cdf(-d1)
        )
        rho = -strike * maturity * df_r * _norm_cdf(-d2)
    gamma = (df_q * pdf) / (spot * vol * math.sqrt(maturity)) if maturity > 0 else 0.0
    vega = spot * df_q * pdf * math.sqrt(maturity)
    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
    }
