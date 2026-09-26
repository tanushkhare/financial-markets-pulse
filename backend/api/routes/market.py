from fastapi import APIRouter, Query
from backend.services.market_service import MarketService

router = APIRouter(prefix="/api/v1/market", tags=["Market"])

@router.get("/latest")
def get_latest():
    return MarketService.get_latest_market_data()

@router.get("/history")
def get_history(symbol: str = Query(..., description="Stock symbol e.g. AAPL"), limit: int = 100):
    return MarketService.get_market_history(symbol, limit)