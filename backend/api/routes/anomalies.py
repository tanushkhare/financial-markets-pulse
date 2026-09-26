from fastapi import APIRouter, Query
from backend.services.market_service import MarketService

router = APIRouter(prefix="/api/v1", tags=["Anomalies"])

@router.get("/anomalies")
def get_anomalies(limit: int = 50):
    return MarketService.get_anomalies(limit)