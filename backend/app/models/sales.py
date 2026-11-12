from datetime import date
from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.models.base import Base

class SalesHistory(Base):
    __tablename__ = "sales_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    unit_sale_price = Column(Float, nullable=False)
    total_revenue = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    gross_profit = Column(Float, nullable=False)
    sale_date = Column(Date, nullable=False, index=True)

    # Relationships
    product = relationship("Product", back_populates="sales_records")
    customer = relationship("Customer", back_populates="sales_records")

