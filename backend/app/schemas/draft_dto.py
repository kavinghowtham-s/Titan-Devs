from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, ConfigDict

class DrafterResponse(BaseModel):
    subject: str = Field(..., description="Contextual reply email subject")
    body: str = Field(..., description="Full reply body matching customer language")
    estimated_delivery_days: Optional[int] = Field(None, description="Estimated days or null")
    discount_offered_pct: float = Field(0.0, description="Authorized discount percentage")
    requires_manager_special_attention: bool = False

class SafetyRuleCheck(BaseModel):
    rule_name: str
    passed: bool
    reason: str

class OrchestratorSafetyEvaluation(BaseModel):
    verdict: Literal["PASS", "FAIL"]
    safety_score: float = Field(0.95, ge=0.0, le=1.0)
    rule_checks: List[SafetyRuleCheck] = Field(default_factory=list)
    escalation_reason: Optional[str] = None
    recommended_action: Literal["auto_approve_and_send", "escalate_to_manager"] = "auto_approve_and_send"

class DraftReplyEdit(BaseModel):
    edited_text: str

class DraftReplyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    inbound_message_id: int
    draft_text: str
    edited_text: Optional[str] = None
    status: str
    confidence_score: float
    safety_evaluation_notes: Optional[str] = None
    auto_approve_deadline: datetime
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    sent_at: Optional[datetime] = None
    created_at: datetime
    seconds_remaining: Optional[int] = None
