from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, ConfigDict

class ExtractedRequirement(BaseModel):
    sku: Optional[str] = Field(None, description="Matched SKU or null if ambiguous")
    product_name_raw: str = Field(..., description="Mentioned item name in text")
    quantity: int = Field(1, description="Quantity requested")

class IntakeClassificationResult(BaseModel):
    language: Literal["en", "ta", "hi", "other"] = "en"
    detected_intent: Literal["price_quote", "bulk_order", "stock_inquiry", "order_status", "complaint", "refund", "general"] = "general"
    sentiment: Literal["positive", "neutral", "negative", "frustrated"] = "neutral"
    priority: Literal["low", "medium", "high", "urgent"] = "medium"
    requirements: List[ExtractedRequirement] = Field(default_factory=list)
    is_prompt_injection: bool = False
    confidence: float = Field(0.95, ge=0.0, le=1.0)

class InboundMessageCreate(BaseModel):
    channel: str = "email"
    sender_address: str
    subject: Optional[str] = None
    raw_text: str

class InboundMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: Optional[int] = None
    channel: str
    sender_address: str
    subject: Optional[str] = None
    raw_text: str
    language: str
    detected_intent: str
    detected_sentiment: str
    priority: str
    prompt_injection_detected: bool
    processing_status: str
    received_at: datetime
