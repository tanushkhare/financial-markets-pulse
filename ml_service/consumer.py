import json
import time
import os
import redis
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
# Force market_ticks to match the simulator
REDIS_CHANNEL = "market_ticks"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "financial_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def run_consumer():
    print("Connecting to Redis...")
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe(REDIS_CHANNEL)
    
    print(f"Subscribed to Redis channel: {REDIS_CHANNEL}. Waiting for market ticks...")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
    history = {sym: [] for sym in symbols}

    for message in pubsub.listen():
        if message['type'] == 'message':
            try:
                data = json.loads(message['data'])
                sym = data['symbol']
                price = float(data['price'])
                volume = int(data['volume'])
                timestamp = datetime.fromtimestamp(data.get('timestamp', time.time()))

                history[sym].append(price)
                if len(history[sym]) > 20:
                    history[sym].pop(0)

                prices_window = history[sym]
                mean_p = sum(prices_window) / len(prices_window)
                variance = sum((p - mean_p) ** 2 for p in prices_window) / len(prices_window)
                volatility = variance ** 0.5
                log_return = (price - prices_window[-1]) / prices_window[-1] if len(prices_window) > 1 else 0.0

                anomaly_score = volatility / (mean_p + 1e-5) * 100
                is_anomaly = bool(anomaly_score > 1.5 or abs(log_return) > 0.015)

                print(f"[ML Consumer] Processed {sym} | Price: ${price:.2f} | Volatility: {volatility:.4f} | Anomaly: {is_anomaly}")

                cursor.execute(
                    """
                    INSERT INTO market_data (time, symbol, price, volume, log_return, volatility, anomaly_score, is_anomaly)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                (timestamp, sym, price, volume, log_return, volatility, anomaly_score, is_anomaly)
                )
                conn.commit()

            except Exception as e:
                print(f"[Error processing message]: {e}")
                try:
                    conn.rollback()
                except:
                    conn = get_db_connection()
                    cursor = conn.cursor()

if __name__ == "__main__":
    run_consumer()
