from datetime import datetime, timezone
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

def get_utc_now():
    return datetime.now(timezone.utc)

class DemandForecastItem(BaseModel):
    product_id: int
    sku: str
    product_name: str
    category: str
    current_stock: int
    forecast_30d_demand: int
    daily_run_rate: float
    stockout_risk_pct: float
    reorder_point: int
    reorder_recommended: bool
    status: Literal["CRITICAL", "WARNING", "HEALTHY"]

class PnLSummary(BaseModel):
    total_sales_volume: int
    total_revenue: float
    total_cogs: float
    total_gross_profit: float
    gross_margin_pct: float
    projected_month_revenue: float
    projected_month_cogs: float
    projected_month_profit: float

class ExecutiveInsight(BaseModel):
    category: Literal["procurement", "revenue_risk", "fast_mover", "margin_optimization"]
    severity: Literal["info", "warning", "critical"]
    finding: str
    recommended_action: str

class ExecutiveBriefingReport(BaseModel):
    headline: str
    executive_summary_markdown: str
    actionable_insights: List[ExecutiveInsight]
    generated_at: datetime = Field(default_factory=get_utc_now)
