from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.app.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sku = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    category = Column(String(64), nullable=False, index=True)
    description = Column(Text, nullable=True)
    unit_selling_price = Column(Float, nullable=False)
    unit_cost_price = Column(Float, nullable=False)
    current_stock = Column(Integer, default=0, nullable=False)
    min_reorder_level = Column(Integer, default=10, nullable=False)
    lead_time_days = Column(Integer, default=5, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    supplier = relationship("Supplier", back_populates="products")
    sales_records = relationship("SalesHistory", back_populates="product")
    stock_order_items = relationship("StockOrderItem", back_populates="product")

