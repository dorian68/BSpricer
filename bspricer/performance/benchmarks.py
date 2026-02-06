from __future__ import annotations

import time

from bspricer.models.black_scholes import price as bs_price
from bspricer.pricing.monte_carlo import price_asian_option_mc
from bspricer.performance.numba_kernels import numba_available


def _time_it(fn, runs: int) -> dict:
    start = time.perf_counter()
    for _ in range(runs):
        fn()
    total = time.perf_counter() - start
    return {
        "runs": runs,
        "total_seconds": total,
        "per_call_ms": (total / runs) * 1000.0 if runs else 0.0,
    }


def run_pricing_benchmarks(
    runs: int = 200,
    mc_runs: int = 5,
    mc_paths: int = 20000,
    mc_steps: int = 100,
) -> dict:
    if numba_available():
        price_asian_option_mc(
            spot=100.0,
            strike=100.0,
            maturity=1.0,
            rate=0.03,
            dividend_yield=0.0,
            vol=0.2,
            option_type="call",
            n_paths=1000,
            steps=20,
            seed=123,
        )

    bs_stats = _time_it(
        lambda: bs_price(
            spot=100.0,
            strike=100.0,
            maturity=1.0,
            rate=0.03,
            dividend_yield=0.0,
            vol=0.2,
            option_type="call",
        ),
        runs,
    )

    mc_stats = _time_it(
        lambda: price_asian_option_mc(
            spot=100.0,
            strike=100.0,
            maturity=1.0,
            rate=0.03,
            dividend_yield=0.0,
            vol=0.2,
            option_type="call",
            n_paths=mc_paths,
            steps=mc_steps,
            seed=42,
        ),
        mc_runs,
    )

    return {
        "numba_enabled": numba_available(),
        "black_scholes": bs_stats,
        "asian_mc": mc_stats,
        "mc_paths": mc_paths,
        "mc_steps": mc_steps,
    }
