from pydantic import BaseModel


class SendSMS(BaseModel):
  phone_number:str
  