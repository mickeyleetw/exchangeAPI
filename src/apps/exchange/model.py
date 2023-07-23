from pydantic import BaseModel
from typing import Optional


class ExChangeResultModel(BaseModel):
    message: str 
    amount: str