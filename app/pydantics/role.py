from pydantic import BaseModel
from typing import Optional

class RoleBase(BaseModel):
    name: str

class RoleInDB(RoleBase):
    id: int

    class Config:
        orm_mode = True

class Role(RoleInDB):
    pass
