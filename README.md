# BSpricer

Institutional-grade pricing and risk analytics showcase for multi-asset derivatives.

This repository is designed as a client-facing portfolio project for institutional pricing work. It provides a clean Python API, a FastAPI service, a Streamlit demo, and performance hooks (Numba and C++ wrapper) for scaling.

Key capabilities
- Multi-asset coverage: equity, FX, rates, credit, and exotics
- Pricing engines: analytic and Monte Carlo
- Risk outputs: greeks, scenarios, stress
- Calibration utilities: implied vol and curve helpers
- Deployment-ready: FastAPI + Streamlit + clean packaging
- Rates and credit pricing: Black-76, swaps, CDS
- Performance benchmarks with Numba and C++ hooks

Quickstart
1. Create a virtual environment and install dependencies.
2. `pip install -e .`
3. Run the API: `uvicorn bspricer.api.main:app --reload`
4. Run the UI: `streamlit run streamlit_app/app.py`

Example API request
```json
{
  "request": {
    "instrument": "equity_option",
    "spot": 100.0,
    "strike": 100.0,
    "maturity": 1.0,
    "rate": 0.03,
    "dividend_yield": 0.01,
    "vol": 0.2,
    "option_type": "call"
  },
  "engine": "analytic"
}
```

Repository layout
- `bspricer/` core pricing library
- `bspricer/api/` FastAPI service
- `streamlit_app/` Streamlit demo
- `cpp/` C++ wrapper (pybind11)
- `docs/` methodology and model governance
- `tests/` unit tests
- `data/` sample data layout

Scope and disclaimer
This is a showcase project using synthetic or public data. It is not investment advice and is not a production trading system.
