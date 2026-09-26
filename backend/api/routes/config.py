from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.market_service import MarketService

router = APIRouter(prefix="/api/v1", tags=["Configuration"])

class ConfigUpdate(BaseModel):
    value: dict

@router.get("/config/{key}")
def get_config(key: str):
    val = MarketService.get_config(key)
    if val is None:
        raise HTTPException(status_code=404, detail="Configuration key not found")
    return {key: val}

@router.patch("/config/{key}")
def patch_config(key: str, payload: ConfigUpdate):
    return MarketService.update_config(key, payload.value)