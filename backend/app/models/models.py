from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionCategory(str, enum.Enum):
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT = "investment"
    FOOD = "food"
    TRANSPORT = "transport"
    HOUSING = "housing"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    SHOPPING = "shopping"
    OTHER = "other"


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)  # 1-12
    year = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(
        Enum(
            TransactionType,
            values_callable=lambda obj: [e.value for e in obj],
            name="transactiontype",
        ),
        nullable=False,
        index=True,
    )
    category = Column(
        Enum(
            TransactionCategory,
            values_callable=lambda obj: [e.value for e in obj],
            name="transactioncategory",
        ),
        nullable=False,
        index=True,
    )
    description = Column(Text, nullable=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    is_recurring = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
