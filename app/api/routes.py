from fastapi import APIRouter
from app.models.item import Item

router = APIRouter()

@router.get("/items", response_model=list[Item])
async def get_items():
    return [
        Item(id=1, name="śrubka", price=0.99),
        Item(id=2, name="młotek", price=12.50)
    ]
