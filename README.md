# 🤖 AI Lead Classifier Service

An AI-powered microservice built with **FastAPI** and **OpenAI / Ollama** that analyzes incoming customer leads, extracts key information (intent, name, contact), assigns priority, and generates structured responses.

---

## 🌟 Features

- **Lead Intent Classification**: Categorizes leads into `pricing_inquiry`, `booking_request`, `general_question`, or `complaint`.
- **Entity Extraction**: Automatically extracts `extracted_name` and `extracted_contact` from raw text.
- **Priority & Escalation Routing**: Assigns `priority` (`high`, `medium`, `low`) and flags `needs_human` intervention.
- **Dynamic LLM Switcher**: Switch seamlessly between OpenAI Cloud (`gpt-4o-mini`) and Local Models (`Ollama`) via `.env` without changing code.
- **OpenAPI / Swagger Specs**: Interactive documentation out of the box.

---

## ⚙️ Configuration & LLM Switching

You can configure the model provider in your `.env` file:

### Option A: Local Ollama (Free, Offline)

    ```env
    LLM_PROVIDER=ollama
    MODEL_NAME=qwen2.5-coder:7b
    OLLAMA_BASE_URL=http://localhost:11434/v1

---

### Option B: OpenAI Cloud (High Accuracy)

LLM_PROVIDER=openai
MODEL_NAME=gpt-4o-mini
OPENAI_API_KEY=sk-proj-your-api-key-here

---

📁 Directory Structure

lead-classifier-service/
├── app/
│   ├── main.py        # FastAPI endpoints & LLM logic
│   ├── models.py      # Pydantic Request/Response models
│   └── schemas.py     # System Prompt templates & JSON schemas
├── .env.example       # Environment configuration template
├── .gitignore         # File exclusions for Git
├── requirements.txt   # Dependency list
└── README.md          # Project documentation

---

🚀 Quick Start

1. Installation

cd lead-classifier-service
python -m pip install -r requirements.txt

2.Configuration
Create a .env file based on .env.example:

    cp .env.example .env

3.Running the Service

Start the server:

    python -m uvicorn app.main:app --reload

---

Interactive Documentation:
 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
