from fastapi import APIRouter, Query
from starlette import status
from typing import Optional

from core.response import default_responses, response_404,response_403
from core.enum import CurrencyEnum
from core.exception import ResourceNotFoundException,EmptyQueryParamsException
from repository.exchange import ExchangeRepo

from .model import ExChangeResultModel

router = APIRouter(prefix='/exchanges', tags=['exchange'], responses=default_responses)



@router.get('', 
    status_code=status.HTTP_200_OK,
    response_model=ExChangeResultModel,
    responses={
        **response_404('Source or Source and Target Currency relation'),
        **response_403('Source or Target or Amount not found')
    },
)
def currency_exchange(
    source: Optional[CurrencyEnum],
    target: Optional[CurrencyEnum],
    amount: Optional[str] = Query(..., regex=r"^\$?[\d,]+(\.\d{1,2})?$"),
)->ExChangeResultModel :
    if not source or not target or not amount:
        raise EmptyQueryParamsException('Source or Target or Amount not found')
    if not ExchangeRepo.is_source_valid(source):
        raise ResourceNotFoundException('Source Currency')
    if not ExchangeRepo.is_target_valid(source, target):
        raise ResourceNotFoundException('Source and Target Currency relation')
    converted_amount = ExchangeRepo.convert_currency(source, target, amount)
    return ExchangeRepo.convert_exchange_result_to_model(message='success', amount=f'${converted_amount}')