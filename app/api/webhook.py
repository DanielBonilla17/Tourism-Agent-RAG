from fastapi import APIRouter, Request, Query, HTTPException, Response
from app.config import settings
from app.services.message_handler import handle_whatsapp_message

router = APIRouter()

@router.get("/")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        print("✅ Webhook verificado exitosamente por Meta")
        return Response(content=hub_challenge, media_type="text/plain")

    print("❌ Error en la verificación del webhook")
    raise HTTPException(status_code=403, detail="Token de verificación inválido")

@router.post("/")
async def receive_message(request:Request):
    body= await request.json()

    import asyncio
    asyncio.create_task(handle_whatsapp_message(body))
    print(f"Mensaje recibido: {body}")
    return {"status":"received"}