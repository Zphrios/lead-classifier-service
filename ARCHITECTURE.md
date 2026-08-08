# System Architecture & Design Pattern

## Overview
This repository contains a lightweight, event-driven AI Microservice designed for automated lead management, classification, and CRM synchronization.

## System Components & Workflow
1. **API Service (`FastAPI`)**:
   - Acts as the core LLM engine wrapper.
   - Endpoint: `POST /classify` (Receives raw messages, runs structured LLM prompts, outputs typed JSON).
   - Dynamic LLM Backend Provider: Configurable via `.env` to route requests to either Local Ollama (`qwen2.5-coder:7b`/`llama3.2`) or Cloud OpenAI (`gpt-4o-mini`).

2. **Data & Schema Layer (`Pydantic`)**:
   - Request: `{message, business_name, business_type, business_context}`
   - Response Schema:
     - `intent_type`: Categorizes intent (`pricing_inquiry`, `booking_request`, `general_question`, `complaint`).
     - `priority`: `high` | `medium` | `low`
     - `needs_human`: `boolean`
     - `extracted_name`: String or `null`
     - `extracted_contact`: String or `null`
     - `suggested_reply`: Generated response context
     - `confidence`: Float (0.0 - 1.0)

3. **Orchestration & Sync Script (`airtable_sync.py`)**:
   - Polling Worker using `pyairtable`.
   - Fetches unprocessed records (`Status = 'New'`), passes them to FastAPI `/classify`, updates Airtable fields, and sets `Status = 'Processed'`.

## Key Architectural Principles
- **Loose Coupling**: The FastAPI service is completely independent of Airtable; it only handles JSON payloads.
- **Provider Agnostic**: OpenAI-compatible client interface allows seamless switching between local models and cloud endpoints.
- **Strict Typing**: All responses rely on JSON Mode enforcement for zero-parsing errors.
