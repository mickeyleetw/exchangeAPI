from pydantic import BaseModel

class ExChangeResultModel(BaseModel):
    message: str 
    amount: str