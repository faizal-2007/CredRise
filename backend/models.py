from pydantic import BaseModel
from datetime import datetime

class UPITransaction(BaseModel):
    transaction_id: str
    user_id: str
    timestamp: datetime
    amount: float
    category: str
    sender_receiver_id: str
    type: str # 'debit' or 'credit'
    status: str
    is_late_payment: bool = False

class PredictionRequest(BaseModel):
    income_consistency: float
    essentials_ratio: float
    late_payment_freq: float
    failed_tx_rate: float
