from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Yahan apni API Key daalein
genai.configure(api_key="AQ.Ab8RN6JISn5dIJG-Pb00ic389xrKRVyFLbkb70vkjwo-0qYzHg")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.post("/extract")
async def extract(request: Request):
    data = await request.json()
    text = data.get("invoice_text", "")
    
    prompt = f"""
    You are an invoice parser. Extract these 6 fields: invoice_no, date, vendor, amount, tax, currency.
    Rules:
    1. If a field is missing, return null.
    2. Date must be YYYY-MM-DD.
    3. Return ONLY a valid JSON object.
    
    Invoice Text: {text}
    """
    
    response = model.generate_content(prompt)
    # response se JSON nikalna
    raw_text = response.text.replace("json", "").replace("", "").strip()
    return json.loads(raw_text)
