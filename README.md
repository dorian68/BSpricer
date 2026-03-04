# BSpricer

Institutional-grade pricing and risk analytics showcase for multi-asset derivatives, designed as a client-facing portfolio project.

**Business Context**
BSpricer mirrors front-office and risk workflows where pricing, hedging, and model validation must be fast, explainable, and reproducible. It focuses on the end-to-end business path from market inputs to pricing, risk measures, and scenario analysis, with delivery channels that match real integration needs (API, UI, performance hooks).

**What This Project Delivers**
- Multi-asset derivatives pricing in equity, FX, rates, and credit.
- Vanilla and exotic option valuation with analytic and Monte Carlo engines.
- Risk outputs for hedging and sensitivity analysis.
- Calibration utilities and market data handling for practical workflows.
- Deployment-ready API and Streamlit demo for stakeholder review.
- Performance acceleration via Numba and an optional C++ extension.

**Instrument Coverage**
- Equity options (vanilla): Black-Scholes valuation and Greeks.
- FX options (vanilla): Garman-Kohlhagen pricing and Greeks.
- Rate options: Black-76 on forwards.
- Exotics: Asian, barrier, and digital options via Monte Carlo.
- Rates: zero-coupon pricing, par swap rate, and fixed-float swap PV.
- Credit: CDS pricing and fair spread with flat hazard rate.

**Quant Models and Methods**
- Black-Scholes for equity option pricing and closed-form Greeks.
- Garman-Kohlhagen for FX options (domestic/foreign rate inputs).
- Black-76 for rate options on forwards.
- Geometric Brownian Motion Monte Carlo for exotic options.
- Flat-curve discounting utilities for rates products.
- Flat hazard-rate CDS valuation for credit risk.
- Implied volatility calibration via Newton method.

**Risk and Analytics Outputs**
- Prices for all supported instruments.
- Greeks: delta, gamma, vega, theta, rho for equity and FX options.
- Scenario analysis: parallel curve shifts for rate sensitivity.
- CDS fair spread calculation for credit pricing.
- Swap analytics: par rate and PV.

**Market Data and Calibration**
- CSV market data provider for spot series and yield curves.
- Flat curve helper for discount factors.
- Implied volatility inversion for quote-to-model workflows.

**Architecture**
- Core library: `bspricer/` with clean, testable APIs.
- API service: FastAPI endpoints for pricing, batch pricing, Greeks, and CDS fair spread.
- UI: Streamlit app with interactive tabs for pricing, Greeks, exotics, rates/credit, and benchmarks.
- Performance: Numba-accelerated Monte Carlo and optional C++ Black-Scholes extension.

**Skills Demonstrated**
- Derivatives valuation: vanilla and exotic options, rate options, credit derivatives.
- Quantitative finance modeling: Black-Scholes, Garman-Kohlhagen, Black-76, hazard-rate CDS.
- Numerical methods: Monte Carlo simulation, implied vol calibration.
- Risk analytics: Greeks, scenario analysis, swap metrics.
- Software engineering: clean API design, validation with Pydantic, testing, packaging.
- Performance engineering: Numba kernels and C++ extension via pybind11.

**Use Cases**
- Front-office quoting: fast, explainable prices for vanilla equity/FX and rate options.
- Structured products: Monte Carlo valuation for barrier, Asian, and digital payoffs.
- Hedging and risk: Greeks for delta-hedging and sensitivity analysis.
- Rates desks: swap PV and par rate calculations from flat curves.
- Credit desks: CDS valuation and fair spread estimation with hazard-rate assumptions.
- Model validation: analytic vs Monte Carlo consistency checks and benchmark timing.
- Integration demos: API and Streamlit UI to showcase pricing workflows to stakeholders.

**Quickstart**
1. Create a virtual environment and install dependencies.
2. `pip install -e .`
3. Run the API: `uvicorn bspricer.api.main:app --reload`
4. Run the UI: `streamlit run streamlit_app/app.py`

**API Endpoints and Response Formats**
`GET /health` returns service status.
```json
{
  "status": "ok"
}
```

`POST /price` prices a single instrument. Supports analytic or Monte Carlo engines where applicable. Exotics are Monte Carlo only.
```json
{
  "price": 10.25,
  "engine": "analytic"
}
```

`POST /batch` prices a list of instruments in one request.
```json
{
  "prices": [10.25, 3.42, 0.88],
  "engine": "analytic"
}
```

`POST /greeks` computes Greeks for equity or FX options.
```json
{
  "greeks": {
    "delta": 0.52,
    "gamma": 0.019,
    "vega": 12.4,
    "theta": -5.3,
    "rho": 42.1
  }
}
```

`POST /credit/fair_spread` computes the fair CDS spread given hazard, recovery, and discount rates.
```json
{
  "fair_spread": 0.0123
}
```

**API Examples**
Analytic equity option pricing:
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

Monte Carlo barrier option pricing:
```json
{
  "request": {
    "instrument": "barrier_option",
    "spot": 100.0,
    "strike": 95.0,
    "maturity": 1.0,
    "rate": 0.03,
    "dividend_yield": 0.0,
    "vol": 0.25,
    "barrier": 120.0,
    "barrier_type": "up-and-out",
    "option_type": "call"
  },
  "engine": "mc",
  "n_paths": 50000,
  "n_steps": 252,
  "seed": 42
}
```

CDS fair spread request:
```json
{
  "maturity": 5.0,
  "payment_frequency": 4,
  "hazard_rate": 0.02,
  "recovery_rate": 0.4,
  "discount_rate": 0.02
}
```

**Glossary**
- **Black-Scholes:** closed-form model for equity option pricing under lognormal dynamics.
- **Garman-Kohlhagen:** FX option model using domestic and foreign interest rates.
- **Black-76:** pricing model for options on forwards or futures.
- **Monte Carlo:** simulation-based pricing by averaging discounted payoffs.
- **Implied Volatility:** volatility level that matches a market price to a model price.
- **Delta:** sensitivity of option value to spot price changes.
- **Gamma:** sensitivity of delta to spot price changes.
- **Vega:** sensitivity of option value to volatility changes.
- **Theta:** sensitivity of option value to time decay.
- **Rho:** sensitivity of option value to interest rate changes.
- **Barrier Option:** option activated or knocked out when a barrier is breached.
- **Asian Option:** option with payoff based on average underlying price.
- **Digital Option:** option with a fixed payout if a condition is met.
- **Hazard Rate:** default intensity used in credit pricing.
- **Recovery Rate:** percentage of notional recovered after default.
- **Discount Factor:** present-value multiplier for future cashflows.
- **Par Swap Rate:** fixed rate that sets swap PV to zero at inception.

**Repository Layout**
- `bspricer/` core pricing library
- `bspricer/api/` FastAPI service
- `streamlit_app/` Streamlit demo
- `cpp/` C++ extension (pybind11)
- `docs/` methodology, model card, and audit trail notes
- `tests/` unit tests for formulas and Monte Carlo
- `data/` example data layout

**Model Governance and Validation**
- `docs/methodology.md` describes scope, models, calibration, and limitations.
- `docs/model_card.md` summarizes intended use and model risks.
- `docs/audit_trail.md` outlines reproducibility and logging practices.
- `tests/` provides regression checks against analytic formulas and MC sanity checks.

**Limitations**
- Simplified market data handling and flat-curve assumptions.
- No volatility surface dynamics or stochastic rates.
- Not suitable for live trading without production controls and governance.

**Disclaimer**
This is a showcase project using synthetic or public data. It is not investment advice and not a production trading system.
