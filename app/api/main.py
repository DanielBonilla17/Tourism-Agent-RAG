from fastapi import FastAPI
from app.api.webhook import router as webhook_router

app= FastAPI(title="Margarita Tourism Agent API")


app.include_router(webhook_router,prefix="/webhook", tags=["Whatsapp Whebhook"])

@app.get("/")
def read_root():
    return {"message": "Servidor del agente activo!"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)

