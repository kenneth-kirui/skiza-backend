from fastapi import APIRouter
from external_api.subscribe_tune import subscribe_tune
from pydantics.subscriber import Subscribe


router = APIRouter(
    tags=['subscribe tune'],
    prefix="/subscribe"
)

@router.post("/")
def send_subscribe_tune(Body:Subscribe):
  print (Body)
  return subscribe_tune(phone_number=Body.phone_number, skiza_code=Body.skiza_code)
  