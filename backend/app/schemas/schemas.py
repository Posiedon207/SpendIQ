from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from app.models.models import TransactionType, TransactionCategory


# ─── Transaction Schemas ────────────────────────────────────────────────────

class TransactionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Transaction title")
    amount: float = Field(..., gt=0, description="Transaction amount (must be positive)")
    transaction_type: TransactionType = Field(..., description="income or expense")
    category: TransactionCategory = Field(..., description="Transaction category")
    description: Optional[str] = Field(None, max_length=1000)
    date: datetime = Field(..., description="Transaction date")
    is_recurring: bool = Field(default=False)

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be positive")
        return round(v, 2)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[float] = Field(None, gt=0)
    transaction_type: Optional[TransactionType] = None
    category: Optional[TransactionCategory] = None
    description: Optional[str] = Field(None, max_length=1000)
    date: Optional[datetime] = None
    is_recurring: Optional[bool] = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("Amount must be positive")
        return round(v, 2) if v is not None else v


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class TransactionListResponse(BaseModel):
    transactions: List[TransactionResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# ─── Budget Schemas ──────────────────────────────────────────────────────────

class BudgetBase(BaseModel):
    category: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000, le=2100)
    description: Optional[str] = Field(None, max_length=500)

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Budget amount must be positive")
        return round(v, 2)


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    amount: Optional[float] = Field(None, gt=0)
    month: Optional[int] = Field(None, ge=1, le=12)
    year: Optional[int] = Field(None, ge=2000, le=2100)
    description: Optional[str] = Field(None, max_length=500)


class BudgetResponse(BudgetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ─── Analytics Schemas ───────────────────────────────────────────────────────

class SpendingSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    transaction_count: int


class CategoryBreakdown(BaseModel):
    category: str
    total: float
    percentage: float
    count: int


class MonthlyAnalytics(BaseModel):
    month: int
    year: int
    income: float
    expenses: float
    net: float
    transaction_count: int


class AnalyticsResponse(BaseModel):
    summary: SpendingSummary
    expense_by_category: List[CategoryBreakdown]
    income_by_category: List[CategoryBreakdown]
    monthly_trend: List[MonthlyAnalytics]


# ─── Health Schemas ──────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str


class ReadinessResponse(BaseModel):
    status: str
    database: str
    message: str
