from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="gowno123 API", version="0.1.0")

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Witaj w gowno123 API — działa po bożemu!"}
