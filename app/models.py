from pydantic import BaseModel
from typing import Optional

class ClassifyRequest(BaseModel):
    message: str
    business_name: str
    business_type: str
    business_context: Optional[str] = ""

class ClassifyResponse(BaseModel):
    intent_type: str
    priority: str
    needs_human: bool
    extracted_name: Optional[str] = None
    extracted_contact: Optional[str] = None
    suggested_reply: str
    confidence: float
    