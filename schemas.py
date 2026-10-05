from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    rooms: list[str] = Field(min_length=1)
    style: str = "Modern"
    notes: Optional[str] = ""


class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    guests: int = Field(gt=0)
    event_type: str = "Birthday"
    venue: str = ""
    preferences: Optional[str] = ""


class RecommendationItem(BaseModel):
    category: str
    name: str
    platform: str
    estimated_price: float
    quantity: int = 1
    reason: str
    search_url: Optional[str] = None


class RecommendationResponse(BaseModel):
    planner_type: str
    budget: float
    total_estimated: float
    remaining_budget: float
    summary: str
    allocations: dict[str, float]
    recommendations: list[RecommendationItem]
    ai_powered: bool = False

    model_config = ConfigDict(extra="allow")


class SessionInfo(BaseModel):
    authenticated: bool
    user_id: Optional[int] = None
    username: Optional[str] = None


class HistoryItem(BaseModel):
    id: int
    planner_type: str
    created_at: str
    response: dict[str, Any]
