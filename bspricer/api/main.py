from __future__ import annotations

from typing import Annotated, Literal, Union
from fastapi import FastAPI
from pydantic import BaseModel, Field

from bspricer.instruments.vanilla import EquityOption, FXOption, RateOption, OptionType
from bspricer.instruments.credit import CreditDefaultSwap
from bspricer.pricing.analytics import (
    price_equity_option,
    price_fx_option,
    greeks_equity_option,
    greeks_fx_option,
)
from bspricer.pricing.monte_carlo import (
    price_asian_option_mc,
    price_barrier_option_mc,
    price_digital_option_mc,
)
from bspricer.pricing.rates import price_rate_option
from bspricer.pricing.credit import price_cds, fair_cds_spread


class EquityOptionRequest(BaseModel):
    instrument: Literal["equity_option"] = "equity_option"
    spot: float
    strike: float
    maturity: float
    rate: float
    dividend_yield: float = 0.0
    vol: float
    option_type: Literal["call", "put"] = "call"


class FXOptionRequest(BaseModel):
    instrument: Literal["fx_option"] = "fx_option"
    spot: float
    strike: float
    maturity: float
    domestic_rate: float
    foreign_rate: float
    vol: float
    option_type: Literal["call", "put"] = "call"


class RateOptionRequest(BaseModel):
    instrument: Literal["rate_option"] = "rate_option"
    forward: float
    strike: float
    maturity: float
    discount_rate: float
    vol: float
    option_type: Literal["call", "put"] = "call"


class BarrierOptionRequest(BaseModel):
    instrument: Literal["barrier_option"] = "barrier_option"
    spot: float
    strike: float
    maturity: float
    rate: float
    dividend_yield: float = 0.0
    vol: float
    barrier: float
    barrier_type: Literal["up-and-out", "down-and-out", "up-and-in", "down-and-in"]
    option_type: Literal["call", "put"] = "call"


class AsianOptionRequest(BaseModel):
    instrument: Literal["asian_option"] = "asian_option"
    spot: float
    strike: float
    maturity: float
    rate: float
    dividend_yield: float = 0.0
    vol: float
    option_type: Literal["call", "put"] = "call"


class DigitalOptionRequest(BaseModel):
    instrument: Literal["digital_option"] = "digital_option"
    spot: float
    strike: float
    maturity: float
    rate: float
    dividend_yield: float = 0.0
    vol: float
    payout: float = 1.0
    option_type: Literal["call", "put"] = "call"


class CDSRequest(BaseModel):
    instrument: Literal["cds"] = "cds"
    notional: float
    spread: float
    maturity: float
    payment_frequency: int = 4
    hazard_rate: float
    recovery_rate: float = 0.4
    discount_rate: float = 0.02


InstrumentRequest = Annotated[
    Union[
        EquityOptionRequest,
        FXOptionRequest,
        RateOptionRequest,
        BarrierOptionRequest,
        AsianOptionRequest,
        DigitalOptionRequest,
        CDSRequest,
    ],
    Field(discriminator="instrument"),
]


class PriceRequest(BaseModel):
    request: InstrumentRequest
    engine: Literal["analytic", "mc"] | None = None
    n_paths: int = 50000
    n_steps: int = 252
    seed: int | None = None


class GreeksRequest(BaseModel):
    request: Union[EquityOptionRequest, FXOptionRequest]


class BatchPriceRequest(BaseModel):
    requests: list[InstrumentRequest]
    engine: Literal["analytic", "mc"] | None = None
    n_paths: int = 50000
    n_steps: int = 252
    seed: int | None = None


class CDSFairSpreadRequest(BaseModel):
    maturity: float
    payment_frequency: int = 4
    hazard_rate: float
    recovery_rate: float = 0.4
    discount_rate: float = 0.02


app = FastAPI(title="BSpricer API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


def _price_single(req: InstrumentRequest, engine: str | None, n_paths: int, n_steps: int, seed: int | None) -> float:
    if isinstance(req, EquityOptionRequest):
        option = EquityOption(
            spot=req.spot,
            strike=req.strike,
            maturity=req.maturity,
            rate=req.rate,
            dividend_yield=req.dividend_yield,
            vol=req.vol,
            option_type=OptionType(req.option_type),
        )
        return price_equity_option(option)
    if isinstance(req, FXOptionRequest):
        option = FXOption(
            spot=req.spot,
            strike=req.strike,
            maturity=req.maturity,
            domestic_rate=req.domestic_rate,
            foreign_rate=req.foreign_rate,
            vol=req.vol,
            option_type=OptionType(req.option_type),
        )
        return price_fx_option(option)
    if isinstance(req, RateOptionRequest):
        option = RateOption(
            forward=req.forward,
            strike=req.strike,
            maturity=req.maturity,
            discount_rate=req.discount_rate,
            vol=req.vol,
            option_type=OptionType(req.option_type),
        )
        return price_rate_option(option)
    if isinstance(req, BarrierOptionRequest):
        return price_barrier_option_mc(
            spot=req.spot,
            strike=req.strike,
            maturity=req.maturity,
            rate=req.rate,
            dividend_yield=req.dividend_yield,
            vol=req.vol,
            barrier=req.barrier,
            barrier_type=req.barrier_type,
            option_type=req.option_type,
            n_paths=n_paths,
            steps=n_steps,
            seed=seed,
        )
    if isinstance(req, AsianOptionRequest):
        return price_asian_option_mc(
            spot=req.spot,
            strike=req.strike,
            maturity=req.maturity,
            rate=req.rate,
            dividend_yield=req.dividend_yield,
            vol=req.vol,
            option_type=req.option_type,
            n_paths=n_paths,
            steps=n_steps,
            seed=seed,
        )
    if isinstance(req, DigitalOptionRequest):
        return price_digital_option_mc(
            spot=req.spot,
            strike=req.strike,
            maturity=req.maturity,
            rate=req.rate,
            dividend_yield=req.dividend_yield,
            vol=req.vol,
            payout=req.payout,
            option_type=req.option_type,
            n_paths=n_paths,
            steps=n_steps,
            seed=seed,
        )
    if isinstance(req, CDSRequest):
        cds = CreditDefaultSwap(
            notional=req.notional,
            spread=req.spread,
            maturity=req.maturity,
            payment_frequency=req.payment_frequency,
            hazard_rate=req.hazard_rate,
            recovery_rate=req.recovery_rate,
            discount_rate=req.discount_rate,
        )
        return price_cds(cds)
    raise ValueError("Unsupported instrument")


@app.post("/price")
def price(request: PriceRequest) -> dict:
    used_engine = request.engine or "analytic"
    price_value = _price_single(request.request, used_engine, request.n_paths, request.n_steps, request.seed)
    return {"price": price_value, "engine": used_engine}


@app.post("/batch")
def batch_price(request: BatchPriceRequest) -> dict:
    used_engine = request.engine or "analytic"
    prices = [
        _price_single(item, used_engine, request.n_paths, request.n_steps, request.seed)
        for item in request.requests
    ]
    return {"prices": prices, "engine": used_engine}


@app.post("/greeks")
def greeks(request: GreeksRequest) -> dict:
    if isinstance(request.request, EquityOptionRequest):
        option = EquityOption(
            spot=request.request.spot,
            strike=request.request.strike,
            maturity=request.request.maturity,
            rate=request.request.rate,
            dividend_yield=request.request.dividend_yield,
            vol=request.request.vol,
            option_type=OptionType(request.request.option_type),
        )
        return {"greeks": greeks_equity_option(option)}
    option = FXOption(
        spot=request.request.spot,
        strike=request.request.strike,
        maturity=request.request.maturity,
        domestic_rate=request.request.domestic_rate,
        foreign_rate=request.request.foreign_rate,
        vol=request.request.vol,
        option_type=OptionType(request.request.option_type),
    )
    return {"greeks": greeks_fx_option(option)}


@app.post("/credit/fair_spread")
def credit_fair_spread(request: CDSFairSpreadRequest) -> dict:
    cds = CreditDefaultSwap(
        notional=1.0,
        spread=0.0,
        maturity=request.maturity,
        payment_frequency=request.payment_frequency,
        hazard_rate=request.hazard_rate,
        recovery_rate=request.recovery_rate,
        discount_rate=request.discount_rate,
    )
    return {"fair_spread": fair_cds_spread(cds)}
