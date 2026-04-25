import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

def train_dummy_model():
    np.random.seed(42)
    n_samples = 1000
    
    income_consistency = np.random.uniform(0.1, 1.0, n_samples)
    essentials_ratio = np.random.uniform(0.1, 0.9, n_samples)
    late_payment_freq = np.random.poisson(2, n_samples)
    failed_tx_rate = np.random.uniform(0, 0.2, n_samples)
    
    # Calculate mock score (300-900)
    score = 500 + (income_consistency * 150) + (essentials_ratio * 150) - (late_payment_freq * 30) - (failed_tx_rate * 50)
    score += np.random.normal(0, 20, n_samples)
    score = np.clip(score, 300, 900)
    
    df = pd.DataFrame({
        'income_consistency': income_consistency,
        'essentials_ratio': essentials_ratio,
        'late_payment_freq': late_payment_freq,
        'failed_tx_rate': failed_tx_rate
    })
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(df, score)
    
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), 'model.pkl'), 'wb') as f:
        pickle.dump(model, f)
        
    print("Mock model trained and saved to backend/ml/model.pkl")

if __name__ == "__main__":
    train_dummy_model()
