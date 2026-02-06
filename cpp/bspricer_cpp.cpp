#include <cmath>
#include <string>
#include <pybind11/pybind11.h>

namespace py = pybind11;

double norm_cdf(double x) {
    return 0.5 * (1.0 + std::erf(x / std::sqrt(2.0)));
}

double black_scholes_price(
    double spot,
    double strike,
    double maturity,
    double rate,
    double dividend_yield,
    double vol,
    const std::string& option_type
) {
    if (maturity <= 0.0 || vol <= 0.0) {
        double intrinsic = option_type == "call" ? spot - strike : strike - spot;
        return intrinsic > 0.0 ? intrinsic : 0.0;
    }
    double vsqrt = vol * std::sqrt(maturity);
    double d1 = (std::log(spot / strike) + (rate - dividend_yield + 0.5 * vol * vol) * maturity) / vsqrt;
    double d2 = d1 - vsqrt;
    double df_r = std::exp(-rate * maturity);
    double df_q = std::exp(-dividend_yield * maturity);
    if (option_type == "call") {
        return spot * df_q * norm_cdf(d1) - strike * df_r * norm_cdf(d2);
    }
    return strike * df_r * norm_cdf(-d2) - spot * df_q * norm_cdf(-d1);
}

PYBIND11_MODULE(bspricer_cpp, m) {
    m.doc() = "BSpricer C++ extension";
    m.def("black_scholes_price", &black_scholes_price, "Black-Scholes price");
}
