from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Literal


RiskLevel = Literal["low", "medium", "high"]


class InvestorProfile(BaseModel):
    user_id: str
    age: int = Field(ge=18, le=120)
    monthly_income: float = Field(gt=0)
    emergency_fund_months: int = Field(ge=0)
    risk_tolerance: RiskLevel
    investment_horizon_years: int = Field(gt=0)


class Holding(BaseModel):
    symbol: str
    quantity: float = Field(gt=0)
    average_cost: float = Field(gt=0)


class Portfolio(BaseModel):
    user_id: str
    cash: float = Field(ge=0)
    holdings: list[Holding] = Field(default_factory=list)


class AdviceRequest(BaseModel):
    user_id: str
    question: str = Field(min_length=3)


class RebalanceAction(BaseModel):
    symbol: str
    action: Literal["buy", "sell", "hold"]
    reason: str


class AgentMessage(BaseModel):
    agent: str
    content: str
