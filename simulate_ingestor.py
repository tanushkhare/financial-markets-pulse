import os
import random
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables or .env file.")

# Force the psycopg2 driver explicitly
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
prices = {sym: random.uniform(100.0, 500.0) for sym in symbols}

print("Ensuring market_data table exists...")
db = SessionLocal()
try:
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS market_data (
            time TIMESTAMPTZ NOT NULL,
            symbol TEXT NOT NULL,
            price DOUBLE PRECISION,
            volume INTEGER,
            volatility DOUBLE PRECISION,
            is_anomaly BOOLEAN DEFAULT FALSE
        );
    """))
    db.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_market_data_symbol_time
        ON market_data (symbol, time DESC);
    """))
    db.commit()
    print("Table check complete.")
except Exception as e:
    db.rollback()
    print(f"[Error] Failed to ensure table exists: {e}")
    raise
finally:
    db.close()

print("Running one ingestion batch...")
db = SessionLocal()
try:
    for sym in symbols:
        change = random.uniform(-3.0, 3.0)
        prices[sym] = max(10.0, prices[sym] + change)
        volume = random.randint(100, 5000)
        price = round(prices[sym], 2)
        volatility = round(abs(change) / prices[sym], 4)
        is_anomaly = volatility > 0.015

        query = text("""
            INSERT INTO market_data (time, symbol, price, volume, volatility, is_anomaly)
            VALUES (NOW(), :symbol, :price, :volume, :volatility, :is_anomaly)
        """)

        db.execute(query, {
            "symbol": sym,
            "price": price,
            "volume": volume,
            "volatility": volatility,
            "is_anomaly": is_anomaly
        })
        print(f"[Ingestor] Inserted {sym} -> Price: ${price} | Vol: {volume} | Volatility: {volatility} | Anomaly: {is_anomaly}")

    db.commit()
    print("Batch committed successfully.")
except Exception as e:
    db.rollback()
    print(f"[Error] Failed to insert batch: {e}")
    raise
finally:
    db.close()
