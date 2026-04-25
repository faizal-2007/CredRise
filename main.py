from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import score, proxy
from database import init_db

app = FastAPI(title="CredRise Score API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(score.router)
app.include_router(proxy.router)

@app.get("/")
def read_root():
    return {"message": "CredRise API is running"}
