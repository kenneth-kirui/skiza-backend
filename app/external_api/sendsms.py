import random
import requests
import json

from core.config import settings


def generate_code():
    return str(random.randint(1000, 9999))

def send_sms(phone_number:str):
  profile_code = settings.SMS_PROFILE_CODE
  sms_url=settings.SMSURL
  sms_api_key = settings.SMSAPIKEY
  url = sms_url #"https://sms.crossgatesolutions.com:18095/v1/bulksms/messages"
  message = generate_code()
  otp = f"ParteNaSkiza verification code: {message}"
  payload = json.dumps({
    "profile_code": profile_code,
    "messages": [
      {
        "mobile_number": phone_number,
        "message": otp,
        "message_type": "transactional"
        }
        ],
        "dlr_callback_url": "http://example.com"
        })
  headers = {
    'Content-Type': 'application/json',
    'api-key':sms_api_key
    }
  response = requests.request("POST", url, headers=headers, data=payload)
  return({"message":message})


