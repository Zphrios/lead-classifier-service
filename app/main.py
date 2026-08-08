from fastapi import FastAPI, HTTPException
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from app.models import ClassifyRequest, ClassifyResponse
from app.schemas import SYSTEM_PROMPT_TEMPLATE

load_dotenv()

# قراءة إعدادات البيئة
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5-coder:7b")

# تهيئة العميل بناءً على المزود المختار
if LLM_PROVIDER == "ollama":
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    client = OpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key="ollama"  # Ollama doesn't enforce API keys
    )
else:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(title="AI Lead Classification Service")

@app.post("/classify", response_model=ClassifyResponse, summary="Classify incoming lead message")
def classify_message(request: ClassifyRequest):
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        business_name=request.business_name,
        business_type=request.business_type,
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
        return ClassifyResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", summary="Health check endpoint")
def health_check():
    return {
        "status": "running",
        "provider": LLM_PROVIDER,
        "model": MODEL_NAME
    }
    