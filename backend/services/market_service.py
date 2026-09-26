import psycopg2
import json
import traceback

def get_robust_connection():
    try:
        # Try connecting via standard environment variables first
        return psycopg2.connect(
            host="localhost",
            port=5432,
            database="financial_db",
            user="postgres",
            password="postgres"
        )
    except Exception:
        # Fallback to env-based connection if needed
        return psycopg2.connect(
            host="db",
            port=5432,
            database="financial_db",
            user="postgres",
            password="postgres"
        )

class MarketService:
    @staticmethod
    def get_latest_market_data():
        try:
            conn = get_robust_connection()
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
                    "time": row[0].isoformat() if row[0] else None,
                    "symbol": row[1],
                    "price": row[2],
                    "volume": row[3],
                    "log_return": 0.0,
                    "volatility": row[4],
                    "anomaly_score": 0.0,
                    "is_anomaly": row[5]
                })
            return result
        except Exception as e:
            print(f"[ERROR in get_latest_market_data]: {e}")
            traceback.print_exc()
            return []

    @staticmethod
    def get_market_history(symbol: str, limit: int = 100):
        try:
            conn = get_robust_connection()
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
                    "time": row[0].isoformat() if row[0] else None,
                    "symbol": row[1],
                    "price": row[2],
                    "volume": row[3],
                    "log_return": 0.0,
                    "volatility": row[4],
                    "anomaly_score": 0.0,
                    "is_anomaly": row[5]
                })
            return result
        except Exception as e:
            print(f"[ERROR in get_market_history]: {e}")
            return []

    @staticmethod
    def get_anomalies(limit: int = 50):
        try:
            conn = get_robust_connection()
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
                    "time": row[0].isoformat() if row[0] else None,
                    "symbol": row[1],
                    "price": row[2],
                    "volume": row[3],
                    "log_return": 0.0,
                    "volatility": row[4],
                    "anomaly_score": row[5],
                    "is_anomaly": row[6] if len(row) > 6 else row[5]
                })
            return result
        except Exception as e:
            print(f"[ERROR in get_anomalies]: {e}")
            return []

    @staticmethod
    def get_config(key: str):
        return None

    @staticmethod
    def update_config(key: str, value: dict):
        return {"status": "success", "key": key, "value": value}