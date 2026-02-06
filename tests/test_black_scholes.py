from bspricer.models.black_scholes import price


def test_black_scholes_call_price():
    value = price(
        spot=100.0,
        strike=100.0,
        maturity=1.0,
        rate=0.05,
        dividend_yield=0.0,
        vol=0.2,
        option_type="call",
    )
    assert abs(value - 10.4506) < 1e-3
