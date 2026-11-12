from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from backend.app.models.base import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    supplier_code = Column(String(32), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    contact_person = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    phone = Column(String(32), nullable=False)
    category = Column(String(64), nullable=False)
    default_lead_time_days = Column(Integer, default=7, nullable=False)
    payment_terms = Column(String(64), default="Net 30", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    products = relationship("Product", back_populates="supplier")
    stock_orders = relationship("StockOrder", back_populates="supplier")

