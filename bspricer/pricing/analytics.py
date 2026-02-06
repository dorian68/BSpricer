from __future__ import annotations

from bspricer.instruments.vanilla import EquityOption, FXOption
from bspricer.models.black_scholes import price as bs_price, greeks as bs_greeks
from bspricer.models.garman_kohlhagen import price as gk_price


def price_equity_option(option: EquityOption) -> float:
    return bs_price(
        spot=option.spot,
        strike=option.strike,
        maturity=option.maturity,
        rate=option.rate,
        dividend_yield=option.dividend_yield,
        vol=option.vol,
        option_type=option.option_type.value,
    )


def greeks_equity_option(option: EquityOption) -> dict:
    return bs_greeks(
        spot=option.spot,
        strike=option.strike,
        maturity=option.maturity,
        rate=option.rate,
        dividend_yield=option.dividend_yield,
        vol=option.vol,
        option_type=option.option_type.value,
    )


def price_fx_option(option: FXOption) -> float:
    return gk_price(
        spot=option.spot,
        strike=option.strike,
        maturity=option.maturity,
        domestic_rate=option.domestic_rate,
        foreign_rate=option.foreign_rate,
        vol=option.vol,
        option_type=option.option_type.value,
    )


def greeks_fx_option(option: FXOption) -> dict:
    return bs_greeks(
        spot=option.spot,
        strike=option.strike,
        maturity=option.maturity,
        rate=option.domestic_rate,
        dividend_yield=option.foreign_rate,
        vol=option.vol,
        option_type=option.option_type.value,
    )
