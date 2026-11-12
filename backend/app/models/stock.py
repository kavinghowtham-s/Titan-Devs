from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.app.models.base import Base

class StockOrder(Base):
    __tablename__ = "stock_orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_number = Column(String(32), unique=True, nullable=False, index=True)
    inbound_message_id = Column(Integer, ForeignKey("inbound_messages.id"), nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    status = Column(String(32), default="draft", nullable=False, index=True) # draft, approved, rejected, sent
    total_estimated_cost = Column(Float, nullable=False)
    manager_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    approved_at = Column(DateTime, nullable=True)

    # Relationships
    supplier = relationship("Supplier", back_populates="stock_orders")
    inbound_message = relationship("InboundMessage", back_populates="stock_orders")
    items = relationship("StockOrderItem", back_populates="stock_order", cascade="all, delete-orphan")

class StockOrderItem(Base):
    __tablename__ = "stock_order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    stock_order_id = Column(Integer, ForeignKey("stock_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    requested_quantity = Column(Integer, nullable=False)
    in_hand_stock = Column(Integer, nullable=False)
    shortfall_quantity = Column(Integer, nullable=False)
    estimated_unit_cost = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relationships
    stock_order = relationship("StockOrder", back_populates="items")
    product = relationship("Product", back_populates="stock_order_items")

