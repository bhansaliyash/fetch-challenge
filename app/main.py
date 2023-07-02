from fastapi import FastAPI
import logging

from .models.receiptModel import Receipt
from .utils.helper import calculateReceiptPoints, generateUniqueReceiptId

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)
receipt_data = {}

@app.post("/receipts/process")
async def processReceipts(receipt: Receipt):
    '''Generate unique id for the receipt'''
    logger.info(f"Generating unique id for receipt: {receipt}")

    receipt_id = generateUniqueReceiptId(str(receipt))

    logger.info(f"Processing receipt: {receipt_id}")

    if str(receipt_id) in receipt_data:  # make sure same receipts are not accepted multiple times

        logger.info(f"Receipt {receipt_id} already scanned")

        return {"id": receipt_id, "message": "Receipt already scanned"}

    logger.info(f"Calculating reward points for receipt: {receipt_id}")

    receipt_data[str(receipt_id)] = {"data": receipt, "points": calculateReceiptPoints(receipt)}

    logger.info(f"Receipt {receipt_id} processed successfully")

    return {"id": receipt_id, "message": "Receipt processed successfully"}

@app.get("/receipts/{id}/points")
async def receiptPoints(id):
    '''Calculate rewards points for the receipt with given id'''
    logger.info(f"Fetching reward points for receipt: {id}")

    return {"reward points": receipt_data[id]["points"]}