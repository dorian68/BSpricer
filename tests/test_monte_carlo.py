from bspricer.pricing.monte_carlo import price_asian_option_mc


def test_asian_mc_positive_price():
    value = price_asian_option_mc(
        spot=100.0,
        strike=100.0,
        maturity=1.0,
        rate=0.03,
        dividend_yield=0.0,
        vol=0.2,
        option_type="call",
        n_paths=2000,
        steps=50,
        seed=42,
    )
    assert value > 0.0
