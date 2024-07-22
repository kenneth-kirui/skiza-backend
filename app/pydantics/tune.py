from pydantic import BaseModel
from typing import Optional

class TuneBase(BaseModel):
    name: str
    code: int
    user_id: int
    file_name: str

class TuneCreate(TuneBase):
    pass
    class Config:
            orm_mode = True

class TuneUpdate(BaseModel):
   name: str
   code: int
   file_name: str

class TuneInDB(TuneBase):
    id: int
    class Config:
        orm_mode = True

class Tune(TuneInDB):
    pass
