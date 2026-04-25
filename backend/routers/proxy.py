from fastapi import APIRouter
from models import PredictionRequest
from ml.credit_scorer import CreditScorer

router = APIRouter()

@router.post("/simulate")
def simulate_score(req: PredictionRequest):
    # Hackathon override for live demonstrations
    scorer = CreditScorer()
    return scorer.predict_score({
        "income_consistency": req.income_consistency,
        "essentials_ratio": req.essentials_ratio,
        "late_payment_freq": req.late_payment_freq,
        "failed_tx_rate": req.failed_tx_rate
    })
