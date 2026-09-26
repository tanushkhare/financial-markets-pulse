import numpy as np
import pandas as pd

class ZScoreNormalizer:
    def __init__(self, window_size=20):
        self.window_size = window_size
        self.history = {}

    def normalize(self, symbol: str, price: float) -> float:
        if symbol not in self.history:
            self.history[symbol] = []
        
        history = self.history[symbol]
        history.append(price)
        
        if len(history) > self.window_size:
            history.pop(0)
            
        if len(history) < 2:
            return 0.0
            
        arr = np.array(history)
        mean = np.mean(arr)
        std = np.std(arr)
        
        if std == 0.0:
            return 0.0
            
        return float((price - mean) / std)