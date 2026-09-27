import traceback
from backend.db.database import get_db_connection


class MarketService:
    @staticmethod
    def get_latest_market_data():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT ON (symbol)
                    time, symbol, price, volume, volatility, is_anomaly
                FROM market_data
                ORDER BY symbol, time DESC;
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            result = []
            for row in rows:
                result.append({
                    "time": row["time"].isoformat() if row["time"] else None,
                    "symbol": row["symbol"],
                    "price": row["price"],
                    "volume": row["volume"],
                    "log_return": 0.0,
                    "volatility": row["volatility"],
                    "anomaly_score": 0.0,
                    "is_anomaly": row["is_anomaly"]
                })
            return result
        except Exception as e:
            print(f"[ERROR in get_latest_market_data]: {e}")
            traceback.print_exc()
            return []

    @staticmethod
    def get_market_history(symbol: str, limit: int = 100):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT time, symbol, price, volume, volatility, is_anomaly
                FROM market_data
                WHERE symbol = %s
                ORDER BY time DESC
                LIMIT %s;
            """, (symbol.upper(), limit))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            result = []
            for row in rows:
                result.append({
                    "time": row["time"].isoformat() if row["time"] else None,
                    "symbol": row["symbol"],
                    "price": row["price"],
                    "volume": row["volume"],
                    "log_return": 0.0,
                    "volatility": row["volatility"],
                    "anomaly_score": 0.0,
                    "is_anomaly": row["is_anomaly"]
                })
            return result
        except Exception as e:
            print(f"[ERROR in get_market_history]: {e}")
            traceback.print_exc()
            return []

    @staticmethod
    def get_anomalies(limit: int = 50):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT time, symbol, price, volume, volatility, is_anomaly
                FROM market_data
                WHERE is_anomaly = TRUE
                ORDER BY time DESC
                LIMIT %s;
            """, (limit,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            result = []
            for row in rows:
                result.append({
                    "time": row["time"].isoformat() if row["time"] else None,
                    "symbol": row["symbol"],
                    "price": row["price"],
                    "volume": row["volume"],
                    "log_return": 0.0,
                    "volatility": row["volatility"],
                    "anomaly_score": row["volatility"],
                    "is_anomaly": row["is_anomaly"]
                })
            return result
        except Exception as e:
            print(f"[ERROR in get_anomalies]: {e}")
            traceback.print_exc()
            return []

    @staticmethod
    def get_config(key: str):
        return None

    @staticmethod
    def update_config(key: str, value: dict):
        return {"status": "success", "key": key, "value": value}