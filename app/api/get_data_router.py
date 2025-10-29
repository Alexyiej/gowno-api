from fastapi import APIRouter

router = APIRouter()

@router.get("/data")
async def get_data():
    return {"posts": ["Hello World", "FastAPI is great!"]}
