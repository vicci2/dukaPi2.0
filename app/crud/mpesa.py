from base64 import b64encode
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import requests # type: ignore
from datetime import datetime
from app.models.mpesa import MPESAStatus, STK_Push
from app.schemas.mpesa import MpesaCallback
import httpx # type: ignore

consumer_key = 'Jlv0wHaUxIkk2rP0XtTYIb1E49UYX2aF7GYgDTk7uRAwMdf8'
consumer_secret = '4A4LIXuje2qfANoEwY7SQ8KffZBSkfPxmA92nUUFpUs89MGHWCnOQvYpOM055GlT'
pass_key = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
saf_url = "https://sandbox.safaricom.co.ke/"
short_code = '174379'
callback_url = 'https://oneshop.co.ke/stk_callback' #temporarily use Brians until i can get my own

# Helper function (transaction)
def get_transaction(db: Session, mRId: str, cRId: str):
    transaction = db.query(STK_Push).filter(STK_Push.merchant_request_id == mRId, STK_Push.checkout_request_id == cRId).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tansaction with MRID {mRId} & CRID {cRId} not found."
        )
    return transaction

def get_access_token():
   
    try:
        if not consumer_key or not consumer_secret:
            raise ValueError("CONSUMER_KEY or CONSUMER_SECRET not set")

        credentials = f"{consumer_key}:{consumer_secret}"
        encoded_credentials = b64encode(credentials.encode()).decode()
        # print(f"Encoded Credentials: {encoded_credentials}") 
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

        url = f"{saf_url}oauth/v1/generate?grant_type=client_credentials"
        
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code != 200:
            print(f"Response body: {response.text}")  
            raise Exception(f"Auth failed: {response.status_code} - {response.text}")

        json_response = response.json()
        
        access_token = json_response.get("access_token")
        if not access_token:
            raise Exception(f"No access token found in the response: {json_response}")
        return access_token

    except Exception as e:
        print(f"Error getting access token: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get access token: {str(e)}")

async def stk_push_sender(mobile:str, amount:float,access_token:str):
    try:
    # Generate stk password $ Timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        stk_password = b64encode((short_code + pass_key + timestamp).encode('utf-8')).decode()
        
        url = f"{saf_url}mpesa/stkpush/v1/processrequest"
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}

        # Define  the request body
        request = {
            "BusinessShortCode": str(short_code),
            "Password": stk_password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": str(mobile),
            "PartyB": short_code,
            "PhoneNumber": str(mobile),
            "CallBackURL": callback_url,
            "AccountReference": "myduka1",
            "TransactionDesc": "Testing STK Push"
        } 

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=request, headers=headers)
        response.raise_for_status()  
       
        # print("Raw response from MPESA:", response.text)
        return response.json()

    except httpx.RequestError as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Error occurred: {str(e)}"}

def check_transaction_status(merchant_request_id: str, checkout_request_id: str, db):
    transaction = get_transaction(db, merchant_request_id, checkout_request_id)
    # print(f"Transaction found:{transaction}")
    if not transaction:
         raise HTTPException(status_code=404, detail="Transaction not found")
    
    return transaction

async def process_stk_push_callback(payload: MpesaCallback, db: Session):
    pass
    try:
        # get transaction
        transaction = get_transaction(db, payload.merchant_request_id, payload.checkout_request_id)
        # print(f"Transaction: {transaction}")
        
        if payload.result_code != "0":
            transaction.status = MPESAStatus.FAILED
            transaction.result_code = payload.result_code
            transaction.result_desc = payload.result_desc
            db.commit()
            return {
                "status": "failure",
                "message": "Transaction failed",
                "result_code": payload.result_code,
                "result_desc": payload.result_desc
            }   
        
        # else we wanna update our transaction status
        transaction.status = MPESAStatus.COMPLETED
        transaction.result_code = payload.result_code
        transaction.result_desc = payload.result_desc
        db.commit()     
        return {
            "status": "success",
            "message": "Transaction completed"
        }
    except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))