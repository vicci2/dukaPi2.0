from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.mpesa import check_transaction_status, get_access_token, process_stk_push_callback as callBack, stk_push_sender as sender
from app.db import getDb
from app.models.mpesa import MPESAStatus, STK_Push
from app.schemas.mpesa import MpesaCallback, STK_PushCreate, STK_PushResponse, STKPushCheckResponse

# Auth Router
daraja_router = APIRouter()

@daraja_router.post('/', response_model=STK_PushResponse)
async def stk_push(transaction: STK_PushCreate, db: Session = Depends(getDb)):
    try:
        token = get_access_token()
        # Make sure to await the asynchronous function stk_push_sender
        response = await sender(transaction.phone_number, transaction.amount,token)
        print("Received STK Push data:", response)

        if "error" in response:
            print(response)
            raise HTTPException(status_code=400, detail=response["error"])
        
        if 'CheckoutRequestID' in response and 'MerchantRequestID' in response:
            try:
                # Add the STK push response to the database
                mpesa_tx = STK_Push(
                    checkout_request_id=response["CheckoutRequestID"],
                    merchant_request_id=response["MerchantRequestID"],
                    phone=transaction.phone_number,
                    amount=transaction.amount,
                    status=MPESAStatus.PENDING  
                )
                db.add(mpesa_tx)
                db.commit()
                db.refresh(mpesa_tx)
                return {
                    "checkout_request_id": response["CheckoutRequestID"],
                    "merchant_request_id": response["MerchantRequestID"],
                    "status": "pending",
                    "response_code": "0",
                    "response_description": "Success. Request accepted for processing",
                    "customer_message": "Please check your phone to complete the payment"
                }
                # return STK_PushResponse(**response) 
            except Exception as e:
                return {"Error": f"Error adding STK push to db {e}"}
        else:
            raise HTTPException(status_code=400, detail="Invalid response from MPESA")
    except ValueError as ve:
        # Handle known exceptions
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f"STK Push error: {str(e)}")  
        # Return a general server error for unknown issues
        raise HTTPException(status_code=500, detail=str(e))
    
@daraja_router.get("/checker", response_model=STKPushCheckResponse)
async def check_stk_push_status(merchant_request_id: str,checkout_request_id: str,db: Session = Depends(getDb)):
    transaction = check_transaction_status(merchant_request_id, checkout_request_id, db)
    
    if not transaction:
        return {
            "success": False,
            "message": "Transaction not found",
            "status": None
        }
    return {
            "success": transaction.status == MPESAStatus.COMPLETED,
        "message": f"Transaction {transaction.status}",
        "status": transaction.status
    }

@daraja_router.post("/callback")
async def stk_push_callback(callback_data: MpesaCallback, db: Session = Depends(getDb)):
    return await callBack(callback_data, db)