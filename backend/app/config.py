import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "backend/.env", os.path.join(os.path.dirname(__file__), "..", "..", ".env"), os.path.join(os.path.dirname(__file__), "..", ".env")),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    DATABASE_URL: str = "sqlite:///./trentar_ops.db"
    SQLITE_WAL_MODE: bool = True

    # LLM Settings (Ollama Cloud API)
    LLM_MOCK: bool = True
    OLLAMA_BASE_URL: str = "https://ollama.com"
    OLLAMA_API_KEY: Optional[str] = None

    # Per-role Model Routing
    MODEL_INTAKE: str = "deepseek-v4.1-flash"
    MODEL_DRAFTER: str = "deepseek-v4.1-flash"
    MODEL_ORCHESTRATOR: str = "deepseek-v4.1-flash"
    MODEL_SQL: str = "kimi-k2.7-code"
    MODEL_INSIGHTS: str = "deepseek-v4.1-flash"

    # Autonomous Auto-Approval Scheduler (E1)
    AUTO_APPROVE_DELAY_MINUTES: int = 1  # Default to 1m for demo walkthrough
    SCHEDULER_INTERVAL_SECONDS: int = 15

    # Outbound Sender Identity
    SENDER_NAME: str = "Rajesh Kumar"
    SENDER_TITLE: str = "Operations Manager"
    SENDER_COMPANY: str = "Trentar Private Limited"
    SENDER_EMAIL: str = "operations@trentar.com"

    # Channels
    ENABLE_SIMULATED_EMAIL: bool = True
    ENABLE_WHATSAPP_STUB: bool = True

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def is_mock_active(self) -> bool:
        """Mock mode is on if LLM_MOCK is true or no API key is set."""
        if self.LLM_MOCK:
            return True
        return not bool(self.OLLAMA_API_KEY)

settings = Settings()
