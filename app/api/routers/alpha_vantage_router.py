from typing import Annotated

from fastapi import APIRouter, Depends

from services.alpha_vantage_service import ExchangeService
from services.security import RoleChecker

router = APIRouter(
    prefix="/api/info",
    tags=["info"]
)

service = ExchangeService()

@router.get("", status_code=200)
async def get_rates(_: Annotated[str, Depends(RoleChecker(allowed_roles=["user"]))]):
    return await service.get_rates()


