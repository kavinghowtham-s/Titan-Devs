from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.config import settings
from backend.app.llm.client import llm_client

router = APIRouter(prefix="/settings", tags=["Settings & Demo Controls"])

class SettingsUpdateRequest(BaseModel):
    use_mock_llm: Optional[bool] = None
    auto_approve_delay_minutes: Optional[int] = None
    sender_name: Optional[str] = None
    sender_title: Optional[str] = None

@router.get("")
def get_settings():
    """Retrieve current runtime configuration."""
    masked_key = f"...{settings.OLLAMA_API_KEY[-4:]}" if settings.OLLAMA_API_KEY and len(settings.OLLAMA_API_KEY) >= 4 else "None"
    return {
        "app_env": settings.APP_ENV,
        "use_mock_llm": settings.is_mock_active,
        "llm_mock_config": settings.LLM_MOCK,
        "api_key_configured": bool(settings.OLLAMA_API_KEY),
        "masked_key": masked_key,
        "auto_approve_delay_minutes": settings.AUTO_APPROVE_DELAY_MINUTES,
        "sender": {
            "name": settings.SENDER_NAME,
            "title": settings.SENDER_TITLE,
            "company": settings.SENDER_COMPANY,
            "email": settings.SENDER_EMAIL
        },
        "models": {
            "intake": settings.MODEL_INTAKE,
            "drafter": settings.MODEL_DRAFTER,
            "orchestrator": settings.MODEL_ORCHESTRATOR,
            "sql": settings.MODEL_SQL,
            "insights": settings.MODEL_INSIGHTS
        }
    }

@router.post("")
def update_settings(payload: SettingsUpdateRequest):
    """Dynamically modify runtime settings."""
    if payload.use_mock_llm is not None:
        settings.LLM_MOCK = payload.use_mock_llm
    if payload.auto_approve_delay_minutes is not None:
        settings.AUTO_APPROVE_DELAY_MINUTES = payload.auto_approve_delay_minutes
    if payload.sender_name is not None:
        settings.SENDER_NAME = payload.sender_name
    if payload.sender_title is not None:
        settings.SENDER_TITLE = payload.sender_title

    return get_settings()

@router.post("/test-connection")
async def test_llm_connection():
    """Test live connectivity for each configured model role."""
    return await llm_client.test_connection()
