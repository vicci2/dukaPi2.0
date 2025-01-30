from typing import Optional
from pydantic import BaseModel

class STK_PushCreate(BaseModel):
    phone_number:str
    amount: float

class STKPushCheckResponse(BaseModel):
    success: bool
    message: str
    status: Optional[str] = None
    
class STK_PushResponse(BaseModel):
    merchant_request_id:str
    checkout_request_id:str
    status:str
    response_code:str='0'
    response_desc:str='Success. Request accepted for processing'
    customer_message: str = "Please check your phone to complete the payment" 


class MpesaCallback(BaseModel):
    merchant_request_id: str
    checkout_request_id: str
    result_code: str
    result_desc: str


