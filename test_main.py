import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """
    اختبار نقطة الفحص /health للتأكد من استجابة السيرفر
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "lead-classifier-service"

def test_classify_schema_contract():
    """
    اختبار نقطة التصنيف /classify للتأكد من صحة الـ JSON Schema المطلوبة لـ n8n
    """
    payload = {
        "message": "Hi, I need to book an appointment tomorrow evening.",
        "business_type": "Clinic",
        "business_name": "Smile Dental Clinic",
        "channel": "web_form",
        "contact_info": "+201012345678",
        "customer_name": "Ahmed"
    }
    
    response = client.post("/classify", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    
    # التأكد من وجود كافة الحقول الثابتة لـ n8n Contract
    assert "intent" in data
    assert "priority" in data
    assert "suggested_reply" in data
    assert "needs_human" in data
    assert "extracted_info" in data
    assert "confidence" in data
    
    # التأكد من أنواع البيانات
    assert isinstance(data["needs_human"], bool)
    assert isinstance(data["confidence"], (int, float))
    assert isinstance(data["extracted_info"], dict)