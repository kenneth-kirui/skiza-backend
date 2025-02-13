from pydantic import BaseModel

class Subscribe(BaseModel):
  phone_number:str
  skiza_code:str
