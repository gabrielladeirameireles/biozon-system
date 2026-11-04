from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/webhooks", tags=["Webhooks & Bots"])

@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    return {"status": "received", "data": data}


