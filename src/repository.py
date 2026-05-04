from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

from .models import InvestorProfile, Portfolio


@dataclass
class InMemoryRepository:
    profiles: Dict[str, InvestorProfile] = field(default_factory=dict)
    portfolios: Dict[str, Portfolio] = field(default_factory=dict)

    def save_profile(self, profile: InvestorProfile) -> None:
        self.profiles[profile.user_id] = profile

    def get_profile(self, user_id: str) -> Optional[InvestorProfile]:
        return self.profiles.get(user_id)

    def save_portfolio(self, portfolio: Portfolio) -> None:
        self.portfolios[portfolio.user_id] = portfolio

    def get_portfolio(self, user_id: str) -> Optional[Portfolio]:
        return self.portfolios.get(user_id)
