from bspricer.instruments.vanilla import EquityOption, FXOption
from bspricer.models.black_scholes import greeks as bs_greeks


def greeks_for_equity_option(option: EquityOption) -> dict:
    return bs_greeks(
        spot=option.spot,
        strike=option.strike,
        maturity=option.maturity,
        rate=option.rate,
        dividend_yield=option.dividend_yield,
        vol=option.vol,
        option_type=option.option_type.value,
    )


def greeks_for_fx_option(option: FXOption) -> dict:
    return bs_greeks(
        spot=option.spot,
        strike=option.strike,
        maturity=option.maturity,
        rate=option.domestic_rate,
        dividend_yield=option.foreign_rate,
        vol=option.vol,
        option_type=option.option_type.value,
    )
