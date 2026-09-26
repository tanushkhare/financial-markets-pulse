import strawberry
from typing import List, Optional
from backend.services.market_service import MarketService

@strawberry.type
class MarketUpdate:
    time: str
    symbol: str
    price: float
    volume: int
    anomaly_score: float
    is_anomaly: bool

@strawberry.type
class Query:
    @strawberry.field
    def market_updates(self, symbol: Optional[str] = None) -> List[MarketUpdate]:
        if symbol:
            raw_data = MarketService.get_market_history(symbol, limit=20)
        else:
            raw_data = MarketService.get_latest_market_data()
            
        return [
            MarketUpdate(
                time=str(row['time']),
                symbol=row['symbol'],
                price=float(row['price']),
                volume=int(row['volume']),
                anomaly_score=float(row['anomaly_score'] or 0.0),
                is_anomaly=bool(row['is_anomaly'])
            )
            for row in raw_data
        ]

schema = strawberry.Schema(query=Query)