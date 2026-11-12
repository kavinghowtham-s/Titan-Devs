import time
import sqlglot
from sqlglot import exp
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.core.database import get_read_only_db
from backend.app.schemas.assistant_dto import SQLQueryRequest, SQLQueryResponse
from backend.app.llm.client import llm_client

router = APIRouter(prefix="/assistant", tags=["Safe Text-to-SQL Assistant"])

ALLOWED_TABLES = {"products", "suppliers", "customers", "sales_history", "stock_orders", "stock_order_items"}
SCHEMA_DDL = """
TABLE products (id INTEGER, sku TEXT, name TEXT, category TEXT, unit_selling_price REAL, unit_cost_price REAL, current_stock INTEGER, min_reorder_level INTEGER);
TABLE suppliers (id INTEGER, name TEXT, category TEXT, default_lead_time_days INTEGER);
TABLE customers (id INTEGER, name TEXT, company_name TEXT, city TEXT, state TEXT);
TABLE sales_history (id INTEGER, product_id INTEGER, customer_id INTEGER, quantity_sold INTEGER, total_revenue REAL, total_cost REAL, gross_profit REAL, sale_date DATE);
TABLE stock_orders (id INTEGER, order_number TEXT, supplier_id INTEGER, status TEXT, total_estimated_cost REAL);
"""

def validate_and_sanitize_sql(sql_query: str) -> str:
    """Parses SQL via AST to guarantee it is strictly read-only and whitelisted."""
    clean_sql = sql_query.strip().rstrip(";")
    try:
        parsed = sqlglot.parse_one(clean_sql, read="sqlite")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL syntax error: {e}")

    # 1. Statement Type Check: Root MUST be SELECT
    if not isinstance(parsed, exp.Select):
        raise HTTPException(status_code=403, detail="Security violation: Only SELECT queries are permitted.")

    # 2. Table Whitelist Check
    tables = {table.name.lower() for table in parsed.find_all(exp.Table)}
    unauthorized_tables = tables - ALLOWED_TABLES
    if unauthorized_tables:
        raise HTTPException(status_code=403, detail=f"Security violation: Table access restricted: {unauthorized_tables}")

    # 3. Ensure LIMIT <= 50
    limit_node = parsed.args.get("limit")
    if limit_node is None:
        parsed = parsed.limit(50)
    else:
        try:
            val = int(limit_node.expression.this)
            if val > 50:
                parsed.set("limit", exp.Limit(this=exp.Literal.number(50)))
        except Exception:
            parsed.set("limit", exp.Limit(this=exp.Literal.number(50)))

    return parsed.sql(dialect="sqlite")

@router.post("/query", response_model=SQLQueryResponse)
async def query_assistant(
    payload: SQLQueryRequest,
    db: Session = Depends(get_read_only_db)
):
    t0 = time.time()
    # Call SQL LLM Agent
    sql_result = await llm_client.generate_sql(
        employee_query=payload.prompt,
        schema_ddl=SCHEMA_DDL,
        language=payload.language or "en"
    )

    safe_sql = validate_and_sanitize_sql(sql_result.sql_query)

    # Execute against read-only SQLite session
    try:
        cursor = db.execute(text(safe_sql))
        columns = list(cursor.keys())
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Execution error on read-only database: {e}")

    elapsed_ms = round((time.time() - t0) * 1000, 1)

    return SQLQueryResponse(
        sql_query=safe_sql,
        explanation=sql_result.explanation_en,
        natural_response=sql_result.natural_response,
        results=results,
        row_count=len(results),
        execution_time_ms=elapsed_ms,
        speech_ready=True
    )
