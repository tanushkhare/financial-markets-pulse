import numpy as np
import pandas as pd

class FeatureEngineer:
    def __init__(self):
        self.price_history = {}

    def compute_features(self, symbol: str, price: float, volume: int) -> dict:
        if symbol not in self.price_history:
            self.price_history[symbol] = []
            
        history = self.price_history[symbol]
        history.append(price)
        
        if len(history) > 60:
            history.pop(0)
            
        series = pd.Series(history)
        
        log_returns = np.log(series / series.shift(1)).fillna(0.0)
        current_log_return = float(log_returns.iloc[-1]) if len(log_returns) > 0 else 0.0
        
        volatility = float(log_returns.rolling(window=5, min_periods=1).std().iloc[-1])
        
        return {
            "log_return": current_log_return,
            "volatility": volatility,
            "price": price,
            "volume": volume
        }