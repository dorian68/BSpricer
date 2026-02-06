from .black_scholes import price as bs_price


def price(
    spot: float,
    strike: float,
    maturity: float,
    domestic_rate: float,
    foreign_rate: float,
    vol: float,
    option_type: str = "call",
) -> float:
    return bs_price(
        spot=spot,
        strike=strike,
        maturity=maturity,
        rate=domestic_rate,
        dividend_yield=foreign_rate,
        vol=vol,
        option_type=option_type,
    )
