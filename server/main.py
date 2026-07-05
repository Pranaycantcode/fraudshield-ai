from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from fraud_service import process_transaction_csv

app = FastAPI(title="FraudShield AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"message": "FraudShield AI API is running"}


@app.post("/predict")
async def predict_fraud(file: UploadFile = File(...)):
    result = await process_transaction_csv(file)
    return result