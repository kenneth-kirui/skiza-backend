import requests
from core.config import settings

def fetch_token():
  print(settings.SAFARICOMAUTHORIZATION)
  safaricom_token_url = settings.SAFARICOMAUTHORIZATION
  username=settings.USERNAME
  password=settings.PASSWORD
  
  response = requests.post(safaricom_token_url, auth=(username,password))
  if response.status_code==200:
    token_data = response.json()
    access_token = token_data.get("access_token")
    return access_token
    
  else:
    print("Failed:", response.status_code, response.text)
  
  
 