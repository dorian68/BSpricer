from __future__ import annotations


try:
    import bspricer_cpp  # type: ignore
except Exception:
    bspricer_cpp = None


def black_scholes_price_cpp(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    option_type: str = "call",
) -> float:
    if bspricer_cpp is None:
        raise RuntimeError("C++ extension not built. See cpp/README.md")
    return bspricer_cpp.black_scholes_price(
        spot,
        strike,
        maturity,
        rate,
        dividend_yield,
        vol,
        option_type,
    )
