from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.app.models.base import Base

class InboundMessage(Base):
    __tablename__ = "inbound_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    channel = Column(String(32), default="email", nullable=False)
    sender_address = Column(String(128), nullable=False)
    subject = Column(String(256), nullable=True)
    raw_text = Column(Text, nullable=False)
    language = Column(String(16), default="en", nullable=False)
    detected_intent = Column(String(64), nullable=False, index=True)
    detected_sentiment = Column(String(32), nullable=False)
    priority = Column(String(16), default="medium", nullable=False, index=True)
    prompt_injection_detected = Column(Boolean, default=False, nullable=False)
    processing_status = Column(String(32), default="received", nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="inbound_messages")
    draft_reply = relationship("DraftReply", back_populates="inbound_message", uselist=False)
    stock_orders = relationship("StockOrder", back_populates="inbound_message")

class DraftReply(Base):
    __tablename__ = "draft_replies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    inbound_message_id = Column(Integer, ForeignKey("inbound_messages.id"), unique=True, nullable=False)
    draft_text = Column(Text, nullable=False)
    edited_text = Column(Text, nullable=True)
    status = Column(String(32), default="pending", nullable=False, index=True) # pending, approved, rejected, auto_approved, escalated, sent
    confidence_score = Column(Float, default=0.90, nullable=False)
    safety_evaluation_notes = Column(Text, nullable=True)
    auto_approve_deadline = Column(DateTime, nullable=False, index=True)
    reviewed_at = Column(DateTime, nullable=True)
    reviewed_by = Column(String(64), nullable=True)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    inbound_message = relationship("InboundMessage", back_populates="draft_reply")
    outbox_message = relationship("OutboxMessage", back_populates="draft_reply", uselist=False)

class OutboxMessage(Base):
    __tablename__ = "outbox_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    draft_reply_id = Column(Integer, ForeignKey("draft_replies.id"), nullable=True)
    channel = Column(String(32), nullable=False)
    recipient_address = Column(String(128), nullable=False)
    subject = Column(String(256), nullable=True)
    body_text = Column(Text, nullable=False)
    dispatched_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    delivery_status = Column(String(32), default="DELIVERED", nullable=False)

    # Relationships
    draft_reply = relationship("DraftReply", back_populates="outbox_message")

