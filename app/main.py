import os
import json
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from dotenv import load_dotenv

from app.schemas import SYSTEM_PROMPT_TEMPLATE, LeadRequest, LeadResponse

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5-coder:7b")

if LLM_PROVIDER == "ollama":
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    client = OpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key="ollama"
    )
else:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(
    title="AI Lead Classifier & Response Service",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "lead-classifier-service",
        "provider": LLM_PROVIDER,
        "model": MODEL_NAME
    }

@app.post("/classify", response_model=LeadResponse)
def classify_message(request: LeadRequest):
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        business_name=request.business_name or "General Business",
        business_type=request.business_type or "General",
        business_context=request.business_context or "No additional context provided."
    )
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        if "intent" not in result and "intent_type" in result:
            result["intent"] = result.pop("intent_type")
            
        if "suggested_reply" not in result:
            result["suggested_reply"] = "Thank you for reaching out."
            
        if "needs_human" not in result:
            result["needs_human"] = False
            
        if "confidence" not in result:
            result["confidence"] = 0.90
            
        if "extracted_info" not in result:
            result["extracted_info"] = {
                "full_name": request.customer_name,
                "contact_info": request.contact_info,
                "preferred_date": None,
                "preferred_time": None
            }

        return LeadResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))