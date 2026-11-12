from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from backend.app.models.base import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_code = Column(String(32), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, index=True)
    phone = Column(String(32), nullable=False)
    company_name = Column(String(128), nullable=False)
    city = Column(String(64), nullable=False)
    state = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    inbound_messages = relationship("InboundMessage", back_populates="customer")
    sales_records = relationship("SalesHistory", back_populates="customer")

