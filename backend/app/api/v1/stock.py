from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.stock import StockOrder, StockOrderItem
from backend.app.models.product import Product
from backend.app.models.supplier import Supplier
from backend.app.models.audit import AuditLog
from backend.app.schemas.stock_dto import StockOrderResponse, StockOrderItemResponse, StockOrderApproveRequest

router = APIRouter(tags=["Stock & Supplier Orders"])

@router.get("/stock-orders", response_model=List[StockOrderResponse])
def list_stock_orders(
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(StockOrder)
    if status:
        query = query.filter(StockOrder.status == status)
    orders = query.order_by(StockOrder.created_at.desc()).all()

    results = []
    for o in orders:
        supplier = db.query(Supplier).filter(Supplier.id == o.supplier_id).first()
        items = []
        for item in o.items:
            prod = db.query(Product).filter(Product.id == item.product_id).first()
            items.append(StockOrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                product_sku=prod.sku if prod else "UNKNOWN",
                product_name=prod.name if prod else "Unknown Item",
                requested_quantity=item.requested_quantity,
                in_hand_stock=item.in_hand_stock,
                shortfall_quantity=item.shortfall_quantity,
                estimated_unit_cost=item.estimated_unit_cost,
                subtotal=item.subtotal
            ))
        results.append(StockOrderResponse(
            id=o.id,
            order_number=o.order_number,
            inbound_message_id=o.inbound_message_id,
            supplier_id=o.supplier_id,
            supplier_name=supplier.name if supplier else "Supplier",
            supplier_email=supplier.email if supplier else "procurement@supplier.in",
            status=o.status,
            total_estimated_cost=o.total_estimated_cost,
            manager_notes=o.manager_notes,
            created_at=o.created_at,
            approved_at=o.approved_at,
            items=items
        ))
    return results

@router.post("/stock-orders/{order_id}/approve", response_model=StockOrderResponse)
def approve_stock_order(
    order_id: int,
    payload: Optional[StockOrderApproveRequest] = None,
    db: Session = Depends(get_db)
):
    order = db.query(StockOrder).filter(StockOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Stock order not found")

    now = datetime.now(timezone.utc)
    order.status = "sent"
    order.approved_at = now
    if payload and payload.manager_notes:
        order.manager_notes = payload.manager_notes

    db.add(AuditLog(
        entity_type="STOCK_ORDER",
        entity_id=order.id,
        action="APPROVED_AND_SENT",
        actor_type="MANAGER",
        actor_id="MANAGER_RAJESH",
        details_json=f'{{"po_number": "{order.order_number}", "supplier_id": {order.supplier_id}, "total_cost": {order.total_estimated_cost}}}',
        timestamp=now
    ))
    db.commit()
    db.refresh(order)

    # Return formatted response
    supplier = db.query(Supplier).filter(Supplier.id == order.supplier_id).first()
    items = []
    for item in order.items:
        prod = db.query(Product).filter(Product.id == item.product_id).first()
        items.append(StockOrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_sku=prod.sku if prod else "UNKNOWN",
            product_name=prod.name if prod else "Unknown Item",
            requested_quantity=item.requested_quantity,
            in_hand_stock=item.in_hand_stock,
            shortfall_quantity=item.shortfall_quantity,
            estimated_unit_cost=item.estimated_unit_cost,
            subtotal=item.subtotal
        ))

    return StockOrderResponse(
        id=order.id,
        order_number=order.order_number,
        inbound_message_id=order.inbound_message_id,
        supplier_id=order.supplier_id,
        supplier_name=supplier.name if supplier else "Supplier",
        supplier_email=supplier.email if supplier else "procurement@supplier.in",
        status=order.status,
        total_estimated_cost=order.total_estimated_cost,
        manager_notes=order.manager_notes,
        created_at=order.created_at,
        approved_at=order.approved_at,
        items=items
    )

@router.get("/inventory")
def list_inventory(
    low_stock_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if low_stock_only:
        query = query.filter(Product.current_stock <= Product.min_reorder_level)
    products = query.order_by(Product.current_stock.asc()).all()
    return [
        {
            "id": p.id,
            "sku": p.sku,
            "name": p.name,
            "category": p.category,
            "unit_selling_price": p.unit_selling_price,
            "unit_cost_price": p.unit_cost_price,
            "current_stock": p.current_stock,
            "min_reorder_level": p.min_reorder_level,
            "lead_time_days": p.lead_time_days,
            "supplier_id": p.supplier_id,
            "is_low_stock": p.current_stock <= p.min_reorder_level
        }
        for p in products
    ]
