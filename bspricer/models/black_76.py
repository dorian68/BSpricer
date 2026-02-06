import math
from .black_scholes import _norm_cdf


def price(
    forward: float,
    strike: float,
    maturity: float,
    discount_rate: float,
    vol: float,
    option_type: str = "call",
) -> float:
    if maturity <= 0.0 or vol <= 0.0:
        return max(0.0, forward - strike) if option_type == "call" else max(0.0, strike - forward)
    vsqrt = vol * math.sqrt(maturity)
    d1 = (math.log(forward / strike) + 0.5 * vol * vol * maturity) / vsqrt
    d2 = d1 - vsqrt
    df = math.exp(-discount_rate * maturity)
    if option_type == "call":
        return df * (forward * _norm_cdf(d1) - strike * _norm_cdf(d2))
    return df * (strike * _norm_cdf(-d2) - forward * _norm_cdf(-d1))
