import os
import hashlib
import hmac

from fastapi import APIRouter, Request, Header, HTTPException, BackgroundTasks
from dotenv import load_dotenv


load_dotenv()

app = APIRouter()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

if not WEBHOOK_SECRET:
    raise ValueError("Webhook_Secret is missing in .env")


@app.post("/webhook")
async def customer_webhook(request: Request, x_signature: str = Header(None)):

    #Signature exists
    if not x_signature:
        raise HTTPException(status_code=401, detail="Missing webhook")

    x_signature = request.headers.get("X-Signature")

    #read raw request
    body = await request.body()

    #Generate expected signature
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    expected_signature = "sha256=" + expected_signature

    #Compare Signature
    if not hmac.compare_digest(expected_signature,x_signature):
        raise HTTPException(status_code=403, detail="Invalid Signature")

    return {"status": "accepted"}
    