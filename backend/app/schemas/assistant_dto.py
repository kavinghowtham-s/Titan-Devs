from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class SQLQueryRequest(BaseModel):
    prompt: str = Field(..., description="Natural language question from employee")
    language: Optional[str] = Field("en", description="Detected language: en, ta, hi")

class SQLAssistantResult(BaseModel):
    sql_query: str = Field(..., description="Valid SQLite SELECT query")
    explanation_en: str = Field(..., description="Technical explanation of the query")
    natural_response: str = Field(..., description="Conversational reply in input language")

class SQLQueryResponse(BaseModel):
    sql_query: str
    explanation: str
    natural_response: str
    results: List[Dict[str, Any]]
    row_count: int
    execution_time_ms: float
    speech_ready: bool = True

