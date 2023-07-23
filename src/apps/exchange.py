from fastapi import APIRouter, Query,Depends
from starlette import status
from typing import Optional

from core.response import default_responses, response_404
from core.enum import CurrencyEnum    
from core.exception import ResourceNotFoundException
from repositories.exchange import ExchangeRepo
from files.exchange_rate import get_exchange_map

from models.exchange import ExChangeResultModel

router = APIRouter(prefix='/exchanges', tags=['exchange'], responses=default_responses)



@router.get('', 
    status_code=status.HTTP_200_OK,
    response_model=ExChangeResultModel,
    responses={
        **response_404('Source or Source and Target Currency relation')
    },
)
async def currency_exchange(
    source: Optional[CurrencyEnum],
    target: Optional[CurrencyEnum],
    amount: Optional[str] = Query(..., regex=r"^\$?[\d,]+(\.\d{1,2})?$"),
    exchange_map: dict = Depends(get_exchange_map)
)->ExChangeResultModel :
    if not ExchangeRepo.is_source_valid(source_currency=source,exchange_map=exchange_map):
        raise ResourceNotFoundException('Source Currency')
    if not ExchangeRepo.is_target_valid(source_currency=source, target_currency=target,exchange_map=exchange_map):
        raise ResourceNotFoundException('Source and Target Currency relation')
    converted_result = ExchangeRepo.convert_currency(source_currency=source, target_currency=target, amount=amount,exchange_map=exchange_map)
    return ExchangeRepo.convert_exchange_result_to_model(message='success', amount=converted_result)