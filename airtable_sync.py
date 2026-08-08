import os
import requests
from dotenv import load_dotenv
from pyairtable import Api

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "Leads")
SERVICE_URL = "http://127.0.0.1:8000/classify"

# تحويل مخرجات AI للقيم الموجودة بالفعل في جدول Airtable
INTENT_MAP = {
    "pricing_inquiry": "Pricing Request",
    "booking_request": "Booking Inquiry",
    "general_question": "Inquiry",
    "complaint": "Support"
}

def process_airtable_leads():
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
        print("❌ Error: AIRTABLE_API_KEY or AIRTABLE_BASE_ID missing in .env")
        return

    api = Api(AIRTABLE_API_KEY)
    table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)

    records = table.all()
    print(f"🔍 Found {len(records)} total lead(s) in table...")

    for record in records:
        fields = record.get("fields", {})
        message = fields.get("Original_Message") or fields.get("Message")
        
        if not message:
            print(f"⚠️ Skipping record {record['id']} - No message found.")
            continue

        payload = {
            "message": message,
            "business_name": "AI Lead Management System",
            "business_type": fields.get("Business_Type", "Technology"),
            "business_context": ""
        }

        try:
            print(f"⚡ Classifying record {record['id']} ({fields.get('Full_Name', 'Lead')})...")
            response = requests.post(SERVICE_URL, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                raw_intent = result.get("intent_type")
                # مطابقة القيمة المعادة مع خيارات Airtable
                mapped_intent = INTENT_MAP.get(raw_intent, "Inquiry")

                raw_priority = result.get("priority", "medium")
                mapped_priority = raw_priority.capitalize() if raw_priority else "Medium"
                if mapped_priority not in ["High", "Medium", "Low"]:
                    mapped_priority = "Medium"

                update_data = {
                    "Intent_Type": mapped_intent,
                    "Priority": mapped_priority
                }

                table.update(record['id'], update_data)
                print(f"✅ Successfully updated record {record['id']} -> Intent: {mapped_intent}, Priority: {mapped_priority}")
            else:
                print(f"⚠️ Service error for record {record['id']}: {response.text}")

        except Exception as e:
            print(f"❌ Failed to process record {record['id']}: {e}")

if __name__ == "__main__":
    process_airtable_leads()
    