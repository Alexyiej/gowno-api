

from fastapi import APIRouter
from .get_data_router import router as get_data_router

router = APIRouter()

router.include_router(get_data_router, prefix="/api")
