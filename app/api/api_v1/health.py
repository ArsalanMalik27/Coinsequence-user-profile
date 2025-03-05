from dependency_injector.wiring import inject
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
@inject
async def get_health() -> str:
    return "success"
