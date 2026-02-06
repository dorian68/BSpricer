from __future__ import annotations

import math
import numpy as np


try:
    from numba import njit
    _NUMBA = True
except Exception:
    _NUMBA = False
    njit = None


def numba_available() -> bool:
    return _NUMBA


if _NUMBA:
    @njit(cache=True)
    def _gbm_paths_numba(spot, rate, dividend_yield, vol, maturity, steps, normals):
        n_paths = normals.shape[0]
        paths = np.empty((n_paths, steps + 1))
        paths[:, 0] = spot
        dt = maturity / steps
        drift = (rate - dividend_yield - 0.5 * vol * vol) * dt
        diffusion = vol * math.sqrt(dt)
        for t in range(1, steps + 1):
            for i in range(n_paths):
                paths[i, t] = paths[i, t - 1] * math.exp(drift + diffusion * normals[i, t - 1])
        return paths
else:
    def _gbm_paths_numba(*args, **kwargs):
        raise RuntimeError("Numba is not available")


def gbm_paths_numba(
    spot: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    maturity: float,
    steps: int,
    n_paths: int,
    seed: int | None = None,
) -> np.ndarray:
    if not _NUMBA:
        raise RuntimeError("Numba is not available")
    rng = np.random.default_rng(seed)
    normals = rng.standard_normal((n_paths, steps))
    return _gbm_paths_numba(spot, rate, dividend_yield, vol, maturity, steps, normals)
