# Methodology

Scope
- Multi-asset pricing with analytic and Monte Carlo engines
- Exotics supported with MC (barrier, Asian, digital)
- Rates and credit pricing with simplified curves and hazard rates

Models
- Black-Scholes for equity options
- Garman-Kohlhagen for FX options
- Black-76 for rate options
- Flat-curve swap and CDS analytics for credit

Calibration
- Implied volatility via Newton method
- Flat curve utilities for discounting

Validation
- Unit tests for key formulas
- MC vs analytic spot checks

Limitations
- Simplified market data handling
- No transaction costs or market impact
- Not suitable for live trading without additional controls
