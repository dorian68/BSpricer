from bspricer.instruments.credit import CreditDefaultSwap
from bspricer.instruments.vanilla import RateOption, OptionType
from bspricer.pricing.credit import price_cds, fair_cds_spread
from bspricer.pricing.rates import price_rate_option


def test_rate_option_positive_price():
    option = RateOption(
        forward=0.03,
        strike=0.025,
        maturity=1.0,
        discount_rate=0.02,
        vol=0.2,
        option_type=OptionType.CALL,
    )
    assert price_rate_option(option) > 0.0


def test_cds_fair_spread_zero_pv():
    base = CreditDefaultSwap(
        notional=1.0,
        spread=0.01,
        maturity=5.0,
        payment_frequency=4,
        hazard_rate=0.02,
        recovery_rate=0.4,
        discount_rate=0.01,
    )
    fair = fair_cds_spread(base)
    cds = CreditDefaultSwap(
        notional=1.0,
        spread=fair,
        maturity=base.maturity,
        payment_frequency=base.payment_frequency,
        hazard_rate=base.hazard_rate,
        recovery_rate=base.recovery_rate,
        discount_rate=base.discount_rate,
    )
    assert abs(price_cds(cds)) < 1e-4
