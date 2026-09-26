import json
import random
import time
import redis

# Connect to Redis container
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
channel = "market_ticks"

symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
prices = {sym: random.uniform(100.0, 500.0) for sym in symbols}

print("Starting Python Market Ingestor Bypass...")
try:
    while True:
        for sym in symbols:
            # Simulate realistic price walk and volume
            change = random.uniform(-2.0, 2.0)
            prices[sym] = max(10.0, prices[sym] + change)
            volume = random.randint(100, 5000)
            
            tick = {
                "symbol": sym,
                "price": round(prices[sym], 2),
                "volume": volume,
                "timestamp": time.time()
            }
            
            r.publish(channel, json.dumps(tick))
            print(f"[Python Ingestor] Published {sym} -> Price: ${tick['price']} | Vol: {volume}")
            
        time.sleep(5)
except KeyboardInterrupt:
    print("Ingestor stopped.")