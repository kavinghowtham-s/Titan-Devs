from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class StockOrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product_sku: Optional[str] = None
    product_name: Optional[str] = None
    requested_quantity: int
    in_hand_stock: int
    shortfall_quantity: int
    estimated_unit_cost: float
    subtotal: float

class StockOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_number: str
    inbound_message_id: Optional[int] = None
    supplier_id: int
    supplier_name: Optional[str] = None
    supplier_email: Optional[str] = None
    status: str
    total_estimated_cost: float
    manager_notes: Optional[str] = None
    created_at: datetime
    approved_at: Optional[datetime] = None
    items: List[StockOrderItemResponse] = []

class StockOrderApproveRequest(BaseModel):
    manager_notes: Optional[str] = None
