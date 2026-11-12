import math
from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.core.database import get_db
from backend.app.models.product import Product
from backend.app.models.sales import SalesHistory
from backend.app.schemas.analytics_dto import DemandForecastItem, PnLSummary, ExecutiveBriefingReport
from backend.app.llm.client import llm_client

router = APIRouter(prefix="/analytics", tags=["Predictive Demand & P&L Analytics"])

@router.get("/demand-forecast", response_model=List[DemandForecastItem])
def get_demand_forecast(
    horizon_days: int = Query(30, ge=7, le=90),
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()
    today = date.today()
    d30 = today - timedelta(days=30)
    d60 = today - timedelta(days=60)
    d90 = today - timedelta(days=90)

    results = []
    for p in products:
        # Sales in last 30 days
        s30 = db.query(func.coalesce(func.sum(SalesHistory.quantity_sold), 0)).filter(
            SalesHistory.product_id == p.id,
            SalesHistory.sale_date >= d30
        ).scalar() or 0

        # Sales in 31-60 days
        s60 = db.query(func.coalesce(func.sum(SalesHistory.quantity_sold), 0)).filter(
            SalesHistory.product_id == p.id,
            SalesHistory.sale_date >= d60,
            SalesHistory.sale_date < d30
        ).scalar() or 0

        # Sales in 61-90 days
        s90 = db.query(func.coalesce(func.sum(SalesHistory.quantity_sold), 0)).filter(
            SalesHistory.product_id == p.id,
            SalesHistory.sale_date >= d90,
            SalesHistory.sale_date < d60
        ).scalar() or 0

        # Weighted daily run rate: 50% recent, 30% mid, 20% older
        m1 = s30 / 30.0
        m2 = s60 / 30.0
        m3 = s90 / 30.0
        daily_rate = round((0.5 * m1) + (0.3 * m2) + (0.2 * m3), 2)
        if daily_rate == 0:
            daily_rate = 0.2

        projected_demand = math.ceil(daily_rate * horizon_days)
        lead_time_demand = daily_rate * p.lead_time_days

        # Stockout risk calculation
        if lead_time_demand > 0:
            deficit = lead_time_demand - p.current_stock
            risk_pct = round(min(100.0, max(0.0, (deficit / lead_time_demand) * 100.0)), 1)
        else:
            risk_pct = 0.0

        rop = math.ceil(lead_time_demand + (p.min_reorder_level * 0.5))
        needs_reorder = p.current_stock <= rop or risk_pct >= 50.0

        status = "CRITICAL" if risk_pct >= 60 else "WARNING" if risk_pct >= 25 else "HEALTHY"

        results.append(DemandForecastItem(
            product_id=p.id,
            sku=p.sku,
            product_name=p.name,
            category=p.category,
            current_stock=p.current_stock,
            forecast_30d_demand=projected_demand,
            daily_run_rate=daily_rate,
            stockout_risk_pct=risk_pct,
            reorder_point=rop,
            reorder_recommended=needs_reorder,
            status=status
        ))

    # Sort critical risk items to top
    results.sort(key=lambda x: x.stockout_risk_pct, reverse=True)
    return results

@router.get("/pnl-summary", response_model=PnLSummary)
def get_pnl_summary(db: Session = Depends(get_db)):
    totals = db.query(
        func.coalesce(func.sum(SalesHistory.quantity_sold), 0),
        func.coalesce(func.sum(SalesHistory.total_revenue), 0.0),
        func.coalesce(func.sum(SalesHistory.total_cost), 0.0),
        func.coalesce(func.sum(SalesHistory.gross_profit), 0.0)
    ).first()

    vol = totals[0] or 0
    rev = round(float(totals[1] or 0.0), 2)
    cogs = round(float(totals[2] or 0.0), 2)
    profit = round(float(totals[3] or 0.0), 2)
    margin = round((profit / rev * 100.0), 1) if rev > 0 else 35.0

    # 30-day projection
    proj_rev = round(rev / 12.0 * 1.08, 2)
    proj_cogs = round(cogs / 12.0 * 1.05, 2)
    proj_profit = round(proj_rev - proj_cogs, 2)

    return PnLSummary(
        total_sales_volume=vol,
        total_revenue=rev,
        total_cogs=cogs,
        total_gross_profit=profit,
        gross_margin_pct=margin,
        projected_month_revenue=proj_rev,
        projected_month_cogs=proj_cogs,
        projected_month_profit=proj_profit
    )

@router.post("/generate-insights", response_model=ExecutiveBriefingReport)
async def generate_executive_insights(db: Session = Depends(get_db)):
    return await llm_client.generate_insights("Sales trends and inventory status for Trentar Pvt Ltd")
