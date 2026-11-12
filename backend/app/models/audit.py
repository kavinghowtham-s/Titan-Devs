from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from backend.app.models.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entity_type = Column(String(64), nullable=False) # DRAFT, STOCK_ORDER, SECURITY, SYSTEM
    entity_id = Column(Integer, nullable=False)
    action = Column(String(64), nullable=False) # CREATED, APPROVED, AUTO_APPROVED, ESCALATED, BLOCKED
    actor_type = Column(String(32), nullable=False) # MANAGER, SYSTEM_ORCHESTRATOR, SYSTEM, INTAKE_AGENT
    actor_id = Column(String(64), nullable=False)
    details_json = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

