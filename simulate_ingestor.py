import os
import random
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables or .env file.")

# Set up SQLAlchemy engine and session for Render TimescaleDB
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
prices = {sym: random.uniform(100.0, 500.0) for sym in symbols}

print("Starting Direct Database Market Ingestor...")
try:
    while True:
        db = SessionLocal()
        try:
            for sym in symbols:
                # Simulate realistic price walk and volume
                change = random.uniform(-3.0, 3.0)
                prices[sym] = max(10.0, prices[sym] + change)
                volume = random.randint(100, 5000)
                price = round(prices[sym], 2)
                volatility = round(abs(change) / prices[sym], 4)
                is_anomaly = volatility > 0.015  # Flag high volatility as anomaly

                # Insert directly into your TimescaleDB hypertable (markets_vscf)
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
                print(f"[Database Ingestor] Inserted {sym} -> Price: ${price} | Vol: {volume} | Volatility: {volatility} | Anomaly: {is_anomaly}")
            
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"[Error] Failed to insert tick into database: {e}")
        finally:
            db.close()
            
        time.sleep(2)
        
except KeyboardInterrupt:
    print("Ingestor stopped.")