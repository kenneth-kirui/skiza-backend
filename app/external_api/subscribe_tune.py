import json
import requests
import uuid
from core.config import settings
from .skiza_token import fetch_token
def subscribe_tune(phone_number, skiza_code):
  token = fetch_token()
  url = settings.SAFARICOMSESSIONIDURL
  subscriber="0" + phone_number[3:]
  guid = str(uuid.uuid4())
  data = {
    "product":"SKIZA",
    "encryption":"none",
    "subscriberNumber":subscriber,
    "productType":"SKIZA_RBT",
    "productCode":skiza_code,
    "cspid":"123"
    }
  headers = {
  'x-correlation-conversationid': f'{guid}',
  'X-MessageID': 'crossgate',
  'X-Source-System': 'dxl-ms-starter',
  'X-App': 'dxl-ms-starter',
  'X-Msisdn': '0718536999',
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {token}' 
  }
  try:
    response =requests.post(url, json=data, headers=headers)
    response_data = response.json()

    if response.status_code == 200:
      return response_data
    else:
      print(f"Error {response.status_code}:{response.text}") 
  except requests.RequestException as e:
    return None
    