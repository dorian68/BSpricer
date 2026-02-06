import streamlit as st

from bspricer.instruments.vanilla import EquityOption, FXOption, RateOption, OptionType
from bspricer.instruments.credit import CreditDefaultSwap
from bspricer.marketdata.curves import FlatCurve
from bspricer.pricing.analytics import price_equity_option, price_fx_option, greeks_equity_option, greeks_fx_option
from bspricer.pricing.monte_carlo import (
    price_asian_option_mc,
    price_barrier_option_mc,
    price_digital_option_mc,
)
from bspricer.pricing.rates import price_rate_option, price_zero_coupon, par_swap_rate, price_fixed_floating_swap
from bspricer.pricing.credit import price_cds, fair_cds_spread
from bspricer.performance.benchmarks import run_pricing_benchmarks


def build_schedule(maturity: float, frequency: int) -> tuple[list[float], float]:
    frequency = max(int(frequency), 1)
    n_payments = max(int(round(maturity * frequency)), 1)
    accrual = maturity / n_payments
    times = [accrual * i for i in range(1, n_payments + 1)]
    return times, accrual


st.set_page_config(page_title="BSpricer", layout="wide")
st.title("BSpricer Pricing Showcase")

(tab_pricing, tab_greeks, tab_exotics, tab_rates, tab_bench) = st.tabs(
    ["Pricing", "Greeks", "Exotics", "Rates & Credit", "Benchmarks"]
)


with tab_pricing:
    st.subheader("Vanilla Options")
    product = st.selectbox("Instrument", ["Equity Option", "FX Option"])
    spot = st.number_input("Spot", value=100.0)
    strike = st.number_input("Strike", value=100.0)
    maturity = st.number_input("Maturity (years)", value=1.0)
    vol = st.number_input("Volatility", value=0.2)
    option_type = st.selectbox("Option Type", ["call", "put"])
    if product == "Equity Option":
        rate = st.number_input("Rate", value=0.03)
        dividend_yield = st.number_input("Dividend Yield", value=0.0)
        option = EquityOption(
            spot=spot,
            strike=strike,
            maturity=maturity,
            rate=rate,
            dividend_yield=dividend_yield,
            vol=vol,
            option_type=OptionType(option_type),
        )
        if st.button("Price Equity Option"):
            st.metric("Price", price_equity_option(option))
    else:
        domestic_rate = st.number_input("Domestic Rate", value=0.03)
        foreign_rate = st.number_input("Foreign Rate", value=0.01)
        option = FXOption(
            spot=spot,
            strike=strike,
            maturity=maturity,
            domestic_rate=domestic_rate,
            foreign_rate=foreign_rate,
            vol=vol,
            option_type=OptionType(option_type),
        )
        if st.button("Price FX Option"):
            st.metric("Price", price_fx_option(option))


with tab_greeks:
    st.subheader("Greeks")
    product = st.selectbox("Instrument", ["Equity Option", "FX Option"], key="greeks_instrument")
    spot = st.number_input("Spot", value=100.0, key="greeks_spot")
    strike = st.number_input("Strike", value=100.0, key="greeks_strike")
    maturity = st.number_input("Maturity (years)", value=1.0, key="greeks_maturity")
    vol = st.number_input("Volatility", value=0.2, key="greeks_vol")
    option_type = st.selectbox("Option Type", ["call", "put"], key="greeks_type")
    if product == "Equity Option":
        rate = st.number_input("Rate", value=0.03, key="greeks_rate")
        dividend_yield = st.number_input("Dividend Yield", value=0.0, key="greeks_dividend")
        option = EquityOption(
            spot=spot,
            strike=strike,
            maturity=maturity,
            rate=rate,
            dividend_yield=dividend_yield,
            vol=vol,
            option_type=OptionType(option_type),
        )
        if st.button("Compute Greeks"):
            st.json(greeks_equity_option(option))
    else:
        domestic_rate = st.number_input("Domestic Rate", value=0.03, key="greeks_domestic")
        foreign_rate = st.number_input("Foreign Rate", value=0.01, key="greeks_foreign")
        option = FXOption(
            spot=spot,
            strike=strike,
            maturity=maturity,
            domestic_rate=domestic_rate,
            foreign_rate=foreign_rate,
            vol=vol,
            option_type=OptionType(option_type),
        )
        if st.button("Compute Greeks", key="greeks_fx"):
            st.json(greeks_fx_option(option))


with tab_exotics:
    st.subheader("Exotic Options")
    exotic = st.selectbox("Exotic Type", ["Asian", "Barrier", "Digital"])
    spot = st.number_input("Spot", value=100.0, key="exotic_spot")
    strike = st.number_input("Strike", value=100.0, key="exotic_strike")
    maturity = st.number_input("Maturity (years)", value=1.0, key="exotic_maturity")
    rate = st.number_input("Rate", value=0.03, key="exotic_rate")
    dividend_yield = st.number_input("Dividend Yield", value=0.0, key="exotic_dividend")
    vol = st.number_input("Volatility", value=0.2, key="exotic_vol")
    option_type = st.selectbox("Option Type", ["call", "put"], key="exotic_type")
    n_paths = st.number_input("Monte Carlo Paths", value=20000, step=5000, key="exotic_paths")
    steps = st.number_input("Time Steps", value=252, step=10, key="exotic_steps")
    if exotic == "Asian":
        if st.button("Price Asian"):
            price = price_asian_option_mc(
                spot=spot,
                strike=strike,
                maturity=maturity,
                rate=rate,
                dividend_yield=dividend_yield,
                vol=vol,
                option_type=option_type,
                n_paths=int(n_paths),
                steps=int(steps),
            )
            st.metric("Price", price)
    elif exotic == "Barrier":
        barrier = st.number_input("Barrier", value=120.0, key="exotic_barrier")
        barrier_type = st.selectbox(
            "Barrier Type",
            ["up-and-out", "down-and-out", "up-and-in", "down-and-in"],
            key="exotic_barrier_type",
        )
        if st.button("Price Barrier"):
            price = price_barrier_option_mc(
                spot=spot,
                strike=strike,
                maturity=maturity,
                rate=rate,
                dividend_yield=dividend_yield,
                vol=vol,
                barrier=barrier,
                barrier_type=barrier_type,
                option_type=option_type,
                n_paths=int(n_paths),
                steps=int(steps),
            )
            st.metric("Price", price)
    else:
        payout = st.number_input("Payout", value=1.0, key="exotic_payout")
        if st.button("Price Digital"):
            price = price_digital_option_mc(
                spot=spot,
                strike=strike,
                maturity=maturity,
                rate=rate,
                dividend_yield=dividend_yield,
                vol=vol,
                payout=payout,
                option_type=option_type,
                n_paths=int(n_paths),
                steps=int(steps),
            )
            st.metric("Price", price)


with tab_rates:
    st.subheader("Rates")
    st.markdown("Rate Option (Black-76)")
    forward = st.number_input("Forward Rate", value=0.03, key="rate_forward")
    strike = st.number_input("Strike", value=0.025, key="rate_strike")
    maturity = st.number_input("Maturity (years)", value=1.0, key="rate_maturity")
    discount_rate = st.number_input("Discount Rate", value=0.02, key="rate_discount")
    vol = st.number_input("Volatility", value=0.2, key="rate_vol")
    option_type = st.selectbox("Option Type", ["call", "put"], key="rate_type")
    if st.button("Price Rate Option"):
        option = RateOption(
            forward=forward,
            strike=strike,
            maturity=maturity,
            discount_rate=discount_rate,
            vol=vol,
            option_type=OptionType(option_type),
        )
        st.metric("Price", price_rate_option(option))

    st.divider()
    st.markdown("Zero-Coupon and Swap")
    curve_rate = st.number_input("Flat Curve Rate", value=0.02, key="curve_rate")
    curve = FlatCurve(curve_rate)
    zcb_face = st.number_input("ZCB Face", value=100.0, key="zcb_face")
    zcb_maturity = st.number_input("ZCB Maturity", value=2.0, key="zcb_maturity")
    if st.button("Price ZCB"):
        st.metric("ZCB Price", price_zero_coupon(zcb_face, zcb_maturity, curve))

    swap_maturity = st.number_input("Swap Maturity", value=5.0, key="swap_maturity")
    swap_freq = st.number_input("Payments per Year", value=2, step=1, key="swap_freq")
    notional = st.number_input("Notional", value=1_000_000.0, key="swap_notional")
    payment_times, accrual = build_schedule(swap_maturity, int(swap_freq))
    par_rate = par_swap_rate(curve, payment_times, accrual)
    fixed_rate = st.number_input("Fixed Rate", value=float(par_rate), key="swap_fixed")
    if st.button("Price Swap"):
        pv = price_fixed_floating_swap(fixed_rate, notional, curve, payment_times, accrual)
        st.metric("Swap PV", pv)
        st.caption(f"Par rate: {par_rate:.6f}")

    st.divider()
    st.subheader("Credit")
    cds_notional = st.number_input("CDS Notional", value=1_000_000.0, key="cds_notional")
    cds_spread_bps = st.number_input("Spread (bps)", value=100.0, key="cds_spread")
    cds_maturity = st.number_input("CDS Maturity", value=5.0, key="cds_maturity")
    cds_freq = st.number_input("Payments per Year", value=4, step=1, key="cds_freq")
    hazard_rate = st.number_input("Hazard Rate", value=0.02, key="cds_hazard")
    recovery_rate = st.number_input("Recovery Rate", value=0.4, key="cds_recovery")
    discount_rate = st.number_input("Discount Rate", value=0.02, key="cds_discount")
    cds = CreditDefaultSwap(
        notional=cds_notional,
        spread=cds_spread_bps / 10000.0,
        maturity=cds_maturity,
        payment_frequency=int(cds_freq),
        hazard_rate=hazard_rate,
        recovery_rate=recovery_rate,
        discount_rate=discount_rate,
    )
    if st.button("Price CDS"):
        pv = price_cds(cds)
        fair = fair_cds_spread(cds)
        st.metric("CDS PV", pv)
        st.caption(f"Fair spread: {fair * 10000.0:.2f} bps")


with tab_bench:
    st.subheader("Performance Benchmarks")
    runs = st.number_input("Analytic Runs", value=200, step=50)
    mc_runs = st.number_input("MC Runs", value=5, step=1)
    mc_paths = st.number_input("MC Paths", value=20000, step=5000)
    mc_steps = st.number_input("MC Steps", value=100, step=10)
    if st.button("Run Benchmarks"):
        results = run_pricing_benchmarks(
            runs=int(runs),
            mc_runs=int(mc_runs),
            mc_paths=int(mc_paths),
            mc_steps=int(mc_steps),
        )
        st.json(results)
