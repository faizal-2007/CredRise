import numpy as np
import pandas as pd
import shap
import pickle
import os
from typing import Dict, Any, List

class CreditScorer:
    def __init__(self, model_path: str = None):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
            
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        self.explainer = shap.TreeExplainer(self.model)
        
        self.feature_names = {
            'income_consistency': 'Steady income deposits',
            'essentials_ratio': 'Focus on essential spending',
            'late_payment_freq': 'Frequency of late payments',
            'failed_tx_rate': 'Failed transaction rate',
        }

    def predict_score(self, user_features: Dict[str, float]) -> Dict[str, Any]:
        df = pd.DataFrame([user_features])
        
        score = int(self.model.predict(df)[0])
        score = max(300, min(900, score))
        
        shap_values = self.explainer.shap_values(df)[0]
        reasons = self._generate_reason_codes(user_features, shap_values)
        
        return {
            "score": score,
            "reasons": reasons
        }

    def _generate_reason_codes(self, features: Dict[str, float], shap_values: List[float]) -> List[Dict[str, Any]]:
        feature_keys = list(features.keys())
        reasons = []
        
        for i, shap_val in enumerate(shap_values):
            feat_key = feature_keys[i]
            feat_name = self.feature_names.get(feat_key, feat_key)
            
            if abs(shap_val) > 5.0:
                direction = "increased" if shap_val > 0 else "decreased"
                impact = "positive" if shap_val > 0 else "negative"
                message = f"{feat_name} {direction} your score by {abs(shap_val):.0f} points."
                
                reasons.append({
                    "feature": feat_key,
                    "impact": impact,
                    "points": round(abs(shap_val)),
                    "message": message
                })
        
        reasons.sort(key=lambda x: x['points'], reverse=True)
        return reasons[:3]
