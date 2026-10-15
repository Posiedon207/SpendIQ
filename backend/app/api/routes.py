import os
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db, check_db_connection
from app.schemas.schemas import (
    HealthResponse, ReadinessResponse,
    TransactionCreate, TransactionUpdate, TransactionResponse, TransactionListResponse,
    BudgetCreate, BudgetUpdate, BudgetResponse,
    AnalyticsResponse
)
from app.services.services import (
    get_transactions, get_transaction, create_transaction,
    update_transaction, delete_transaction,
    get_budgets, get_budget, create_budget,
    update_budget, delete_budget,
    get_analytics
)

router = APIRouter()

APP_VERSION = "1.0.0"
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")


# ─── Health & Readiness ──────────────────────────────────────────────────────

@router.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Application health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=APP_VERSION,
        environment=ENVIRONMENT,
    )


@router.get("/ready", response_model=ReadinessResponse, tags=["Health"])
def readiness_check():
    """Readiness check — verifies database connectivity."""
    db_ok = check_db_connection()
    if not db_ok:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )
    return ReadinessResponse(
        status="ready",
        database="connected",
        message="All systems operational",
    )


# ─── Transactions ────────────────────────────────────────────────────────────

@router.get("/api/transactions", response_model=TransactionListResponse, tags=["Transactions"])
def list_transactions(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    transaction_type: Optional[str] = Query(None, description="Filter by type: income | expense"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search by title"),
    start_date: Optional[datetime] = Query(None, description="Filter from date (ISO 8601)"),
    end_date: Optional[datetime] = Query(None, description="Filter to date (ISO 8601)"),
    db: Session = Depends(get_db),
):
    """List transactions with filtering and pagination."""
    skip = (page - 1) * page_size
    transactions, total = get_transactions(
        db, skip=skip, limit=page_size,
        transaction_type=transaction_type,
        category=category, search=search,
        start_date=start_date, end_date=end_date,
    )
    total_pages = (total + page_size - 1) // page_size
    return TransactionListResponse(
        transactions=transactions,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.post("/api/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED, tags=["Transactions"])
def create_new_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """Create a new financial transaction."""
    return create_transaction(db, transaction)


@router.get("/api/transactions/{transaction_id}", response_model=TransactionResponse, tags=["Transactions"])
def get_single_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get a specific transaction by ID."""
    tx = get_transaction(db, transaction_id)
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction {transaction_id} not found")
    return tx


@router.put("/api/transactions/{transaction_id}", response_model=TransactionResponse, tags=["Transactions"])
def update_existing_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing transaction."""
    tx = update_transaction(db, transaction_id, transaction_update)
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction {transaction_id} not found")
    return tx


@router.delete("/api/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Transactions"])
def delete_existing_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Delete a transaction."""
    deleted = delete_transaction(db, transaction_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction {transaction_id} not found")


# ─── Budgets ─────────────────────────────────────────────────────────────────

@router.get("/api/budgets", response_model=list[BudgetResponse], tags=["Budgets"])
def list_budgets(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2000, le=2100),
    db: Session = Depends(get_db),
):
    """List budgets, optionally filtered by month and year."""
    return get_budgets(db, month=month, year=year)


@router.post("/api/budgets", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED, tags=["Budgets"])
def create_new_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    """Create a new monthly budget."""
    return create_budget(db, budget)


@router.get("/api/budgets/{budget_id}", response_model=BudgetResponse, tags=["Budgets"])
def get_single_budget(budget_id: int, db: Session = Depends(get_db)):
    """Get a specific budget by ID."""
    b = get_budget(db, budget_id)
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Budget {budget_id} not found")
    return b


@router.put("/api/budgets/{budget_id}", response_model=BudgetResponse, tags=["Budgets"])
def update_existing_budget(budget_id: int, budget_update: BudgetUpdate, db: Session = Depends(get_db)):
    """Update an existing budget."""
    b = update_budget(db, budget_id, budget_update)
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Budget {budget_id} not found")
    return b


@router.delete("/api/budgets/{budget_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Budgets"])
def delete_existing_budget(budget_id: int, db: Session = Depends(get_db)):
    """Delete a budget."""
    deleted = delete_budget(db, budget_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Budget {budget_id} not found")


# ─── Analytics ───────────────────────────────────────────────────────────────

@router.get("/api/analytics", response_model=AnalyticsResponse, tags=["Analytics"])
def get_spending_analytics(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
):
    """Get spending analytics including summary, category breakdown, and monthly trends."""
    return get_analytics(db, start_date=start_date, end_date=end_date)


# ─── Sample Data Seeding ─────────────────────────────────────────────────────

@router.post("/api/seed", tags=["Utility"], status_code=status.HTTP_201_CREATED)
def seed_sample_data(db: Session = Depends(get_db)):
    """Seed the database with sample financial data for demonstration."""
    from app.models.models import Transaction as TxModel, TransactionType as TxType, TransactionCategory as TxCat
    from datetime import timedelta

    existing = db.query(TxModel).count()
    if existing > 0:
        return {"message": f"Database already has {existing} transactions. Skipping seed."}

    now = datetime.utcnow()
    samples = [
        TxModel(title="Monthly Salary", amount=85000.0, transaction_type=TxType.INCOME, category=TxCat.SALARY, date=now - timedelta(days=1), description="October salary"),
        TxModel(title="Freelance Project", amount=15000.0, transaction_type=TxType.INCOME, category=TxCat.FREELANCE, date=now - timedelta(days=5)),
        TxModel(title="Grocery Shopping", amount=3200.0, transaction_type=TxType.EXPENSE, category=TxCat.FOOD, date=now - timedelta(days=2)),
        TxModel(title="Uber Ride", amount=450.0, transaction_type=TxType.EXPENSE, category=TxCat.TRANSPORT, date=now - timedelta(days=3)),
        TxModel(title="Netflix Subscription", amount=649.0, transaction_type=TxType.EXPENSE, category=TxCat.ENTERTAINMENT, date=now - timedelta(days=7)),
        TxModel(title="Electricity Bill", amount=2100.0, transaction_type=TxType.EXPENSE, category=TxCat.UTILITIES, date=now - timedelta(days=10)),
        TxModel(title="Rent Payment", amount=25000.0, transaction_type=TxType.EXPENSE, category=TxCat.HOUSING, date=now - timedelta(days=1), is_recurring=True),
        TxModel(title="Stock Dividends", amount=5200.0, transaction_type=TxType.INCOME, category=TxCat.INVESTMENT, date=now - timedelta(days=15)),
        TxModel(title="Doctor Visit", amount=800.0, transaction_type=TxType.EXPENSE, category=TxCat.HEALTHCARE, date=now - timedelta(days=12)),
        TxModel(title="Online Course", amount=4999.0, transaction_type=TxType.EXPENSE, category=TxCat.EDUCATION, date=now - timedelta(days=20)),
    ]
    db.add_all(samples)
    db.commit()
    return {"message": f"Seeded {len(samples)} sample transactions successfully"}
