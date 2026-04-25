from fastapi import APIRouter
from models import PredictionRequest
from ml.credit_scorer import CreditScorer

router = APIRouter()

scorer = None

@router.on_event("startup")
def load_scorer():
    global scorer
    try:
        scorer = CreditScorer()
    except Exception as e:
        print(f"Model not trained or available: {e}")

@router.post("/score")
def get_user_score(req: PredictionRequest):
    if not scorer:
        return {"error": "Scoring engine offline."}
    
    result = scorer.predict_score({
        "income_consistency": req.income_consistency,
        "essentials_ratio": req.essentials_ratio,
        "late_payment_freq": req.late_payment_freq,
        "failed_tx_rate": req.failed_tx_rate
    })
    
    return result
