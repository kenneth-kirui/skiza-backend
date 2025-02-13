from fastapi import APIRouter
from pydantics.sendSMS import SendSMS
from external_api.sendsms import send_sms


router = APIRouter(
    tags=['messages'],
    prefix="/sms"
)

@router.post("/")
def send_sms_handler(Body:SendSMS):
  code = send_sms(Body.phone_number)
  return code