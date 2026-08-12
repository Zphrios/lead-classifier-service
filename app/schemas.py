from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# قالب الـ System Prompt باللغة الإنجليزية لضمان مخرجات مستقرة
SYSTEM_PROMPT_TEMPLATE = """You are an AI Lead Classifier for {business_name} ({business_type}).
Business Context: {business_context}

Analyze the incoming customer message and respond with a JSON object containing:
1. "intent": The intent of the lead (e.g., "Booking Inquiry", "Pricing Request", "Inquiry", "Support", "Quote Request").
2. "priority": Priority level ("High", "Medium", "Low").
3. "extracted_info": An object with "full_name", "contact_info", "preferred_date", and "preferred_time".
4. "suggested_reply": A professional response in the same language as the customer message.
5. "confidence": A float between 0.0 and 1.0 indicating confidence.
6. "needs_human": Boolean (true if complaint, urgent, or human escalation is needed).
7. "reason": Short explanation for your classification.

Return ONLY valid JSON matching this schema.
"""

class ExtractedInfo(BaseModel):
    full_name: Optional[str] = None
    contact_info: Optional[str] = None
    preferred_date: Optional[str] = None
    preferred_time: Optional[str] = None

class LeadRequest(BaseModel):
    message: str = Field(..., description="Customer input message")
    business_type: Optional[str] = Field("Clinic", description="Business vertical")
    business_name: Optional[str] = Field("Smile Dental Clinic", description="Business name")
    business_context: Optional[str] = Field("", description="Business context/rules")
    channel: Optional[str] = Field("web_form", description="Lead channel")
    contact_info: Optional[str] = Field(None, description="Contact phone or email")
    customer_name: Optional[str] = Field(None, description="Customer name")

class LeadResponse(BaseModel):
    intent: str = Field(...)
    priority: str = Field(...)
    extracted_info: ExtractedInfo = Field(default_factory=ExtractedInfo)
    suggested_reply: str = Field(...)
    confidence: float = Field(0.95)
    needs_human: bool = Field(False)
    reason: Optional[str] = Field(None)