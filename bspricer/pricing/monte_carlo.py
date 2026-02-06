from __future__ import annotations

import math
import numpy as np
from bspricer.performance.numba_kernels import gbm_paths_numba, numba_available


def _gbm_paths_numpy(
    spot: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    maturity: float,
    steps: int,
    n_paths: int,
    seed: int | None = None,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    dt = maturity / steps
    drift = (rate - dividend_yield - 0.5 * vol * vol) * dt
    diffusion = vol * math.sqrt(dt)
    paths = np.empty((n_paths, steps + 1))
    paths[:, 0] = spot
    for t in range(1, steps + 1):
        z = rng.standard_normal(n_paths)
        paths[:, t] = paths[:, t - 1] * np.exp(drift + diffusion * z)
    return paths


def simulate_gbm_paths(
    spot: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    maturity: float,
    steps: int,
    n_paths: int,
    seed: int | None = None,
) -> np.ndarray:
    if numba_available():
        return gbm_paths_numba(spot, rate, dividend_yield, vol, maturity, steps, n_paths, seed)
    return _gbm_paths_numpy(spot, rate, dividend_yield, vol, maturity, steps, n_paths, seed)


def price_asian_option_mc(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    option_type: str = "call",
    n_paths: int = 50000,
    steps: int = 252,
    seed: int | None = None,
) -> float:
    paths = simulate_gbm_paths(spot, rate, dividend_yield, vol, maturity, steps, n_paths, seed)
    avg_price = paths[:, 1:].mean(axis=1)
    if option_type == "call":
        payoff = np.maximum(avg_price - strike, 0.0)
    else:
        payoff = np.maximum(strike - avg_price, 0.0)
    return math.exp(-rate * maturity) * float(np.mean(payoff))


def price_barrier_option_mc(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    barrier: float,
    barrier_type: str,
    option_type: str = "call",
    n_paths: int = 50000,
    steps: int = 252,
    seed: int | None = None,
) -> float:
    paths = simulate_gbm_paths(spot, rate, dividend_yield, vol, maturity, steps, n_paths, seed)
    if "up" in barrier_type:
        touched = paths.max(axis=1) >= barrier
    else:
        touched = paths.min(axis=1) <= barrier
    if "out" in barrier_type:
        active = ~touched
    else:
        active = touched
    terminal = paths[:, -1]
    if option_type == "call":
        payoff = np.maximum(terminal - strike, 0.0)
    else:
        payoff = np.maximum(strike - terminal, 0.0)
    payoff = payoff * active
    return math.exp(-rate * maturity) * float(np.mean(payoff))


def price_digital_option_mc(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    payout: float = 1.0,
    option_type: str = "call",
    n_paths: int = 50000,
    steps: int = 252,
    seed: int | None = None,
) -> float:
    paths = simulate_gbm_paths(spot, rate, dividend_yield, vol, maturity, steps, n_paths, seed)
    terminal = paths[:, -1]
    if option_type == "call":
        payoff = (terminal > strike).astype(float) * payout
    else:
        payoff = (terminal < strike).astype(float) * payout
    return math.exp(-rate * maturity) * float(np.mean(payoff))
