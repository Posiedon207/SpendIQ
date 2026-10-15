from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, desc

from app.models.models import Transaction, Budget, TransactionType
from app.schemas.schemas import (
    TransactionCreate, TransactionUpdate,
    BudgetCreate, BudgetUpdate,
    SpendingSummary, CategoryBreakdown,
    MonthlyAnalytics, AnalyticsResponse
)


# ─── Transaction Services ────────────────────────────────────────────────────

def get_transactions(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    transaction_type: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> tuple[List[Transaction], int]:
    query = db.query(Transaction)

    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    if category:
        query = query.filter(Transaction.category == category)
    if search:
        query = query.filter(Transaction.title.ilike(f"%{search}%"))
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    total = query.count()
    transactions = query.order_by(desc(Transaction.date)).offset(skip).limit(limit).all()
    return transactions, total


def get_transaction(db: Session, transaction_id: int) -> Optional[Transaction]:
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()


def create_transaction(db: Session, transaction: TransactionCreate) -> Transaction:
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_transaction(
    db: Session,
    transaction_id: int,
    transaction_update: TransactionUpdate
) -> Optional[Transaction]:
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction:
        return None
    update_data = transaction_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int) -> bool:
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction:
        return False
    db.delete(db_transaction)
    db.commit()
    return True


# ─── Budget Services ─────────────────────────────────────────────────────────

def get_budgets(db: Session, month: Optional[int] = None, year: Optional[int] = None) -> List[Budget]:
    query = db.query(Budget)
    if month:
        query = query.filter(Budget.month == month)
    if year:
        query = query.filter(Budget.year == year)
    return query.all()


def get_budget(db: Session, budget_id: int) -> Optional[Budget]:
    return db.query(Budget).filter(Budget.id == budget_id).first()


def create_budget(db: Session, budget: BudgetCreate) -> Budget:
    db_budget = Budget(**budget.model_dump())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


def update_budget(db: Session, budget_id: int, budget_update: BudgetUpdate) -> Optional[Budget]:
    db_budget = get_budget(db, budget_id)
    if not db_budget:
        return None
    update_data = budget_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_budget, key, value)
    db.commit()
    db.refresh(db_budget)
    return db_budget


def delete_budget(db: Session, budget_id: int) -> bool:
    db_budget = get_budget(db, budget_id)
    if not db_budget:
        return False
    db.delete(db_budget)
    db.commit()
    return True


# ─── Analytics Services ──────────────────────────────────────────────────────

def get_analytics(
    db: Session,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> AnalyticsResponse:
    query = db.query(Transaction)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    transactions = query.all()

    total_income = sum(t.amount for t in transactions if t.transaction_type == TransactionType.INCOME)
    total_expenses = sum(t.amount for t in transactions if t.transaction_type == TransactionType.EXPENSE)

    summary = SpendingSummary(
        total_income=round(total_income, 2),
        total_expenses=round(total_expenses, 2),
        net_balance=round(total_income - total_expenses, 2),
        transaction_count=len(transactions),
    )

    # Expense by category
    expense_transactions = [t for t in transactions if t.transaction_type == TransactionType.EXPENSE]
    expense_categories: dict = {}
    for t in expense_transactions:
        cat = t.category.value if hasattr(t.category, 'value') else str(t.category)
        if cat not in expense_categories:
            expense_categories[cat] = {"total": 0.0, "count": 0}
        expense_categories[cat]["total"] += t.amount
        expense_categories[cat]["count"] += 1

    expense_by_category = [
        CategoryBreakdown(
            category=cat,
            total=round(data["total"], 2),
            percentage=round((data["total"] / total_expenses * 100) if total_expenses > 0 else 0, 2),
            count=data["count"],
        )
        for cat, data in expense_categories.items()
    ]

    # Income by category
    income_transactions = [t for t in transactions if t.transaction_type == TransactionType.INCOME]
    income_categories: dict = {}
    for t in income_transactions:
        cat = t.category.value if hasattr(t.category, 'value') else str(t.category)
        if cat not in income_categories:
            income_categories[cat] = {"total": 0.0, "count": 0}
        income_categories[cat]["total"] += t.amount
        income_categories[cat]["count"] += 1

    income_by_category = [
        CategoryBreakdown(
            category=cat,
            total=round(data["total"], 2),
            percentage=round((data["total"] / total_income * 100) if total_income > 0 else 0, 2),
            count=data["count"],
        )
        for cat, data in income_categories.items()
    ]

    # Monthly trend (last 12 months)
    monthly_data: dict = {}
    for t in transactions:
        key = (t.date.year, t.date.month)
        if key not in monthly_data:
            monthly_data[key] = {"income": 0.0, "expenses": 0.0, "count": 0}
        if t.transaction_type == TransactionType.INCOME:
            monthly_data[key]["income"] += t.amount
        else:
            monthly_data[key]["expenses"] += t.amount
        monthly_data[key]["count"] += 1

    monthly_trend = [
        MonthlyAnalytics(
            month=month,
            year=year,
            income=round(data["income"], 2),
            expenses=round(data["expenses"], 2),
            net=round(data["income"] - data["expenses"], 2),
            transaction_count=data["count"],
        )
        for (year, month), data in sorted(monthly_data.items())
    ]

    return AnalyticsResponse(
        summary=summary,
        expense_by_category=expense_by_category,
        income_by_category=income_by_category,
        monthly_trend=monthly_trend,
    )
