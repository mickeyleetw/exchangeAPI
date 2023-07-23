from decimal import Decimal
from core.enum import CurrencyEnum

from models.exchange import ExChangeResultModel
from core.exception import ResourceNotFoundException


class ExchangeRepo:
    
    @staticmethod
    def is_source_valid(source_currency:CurrencyEnum,exchange_map:dict)->bool:
        if source_currency not in exchange_map['currencies'].keys():
            return False
        return True
    
    @staticmethod
    def is_target_valid(source_currency:CurrencyEnum,target_currency:CurrencyEnum,exchange_map:dict)->bool:
        if target_currency not in exchange_map['currencies'][source_currency].keys():
            return False
        return True

    @staticmethod
    def convert_currency(source_currency:CurrencyEnum, target_currency:CurrencyEnum, amount:str,exchange_map:dict )->str:
        rate=exchange_map['currencies'][source_currency].get(target_currency,None)
        if not rate:
            raise ResourceNotFoundException('Rate')
        converted_amount = round(Decimal(amount.replace('$', '').replace(',','')) * Decimal(rate), 2)
        return '${:,.2f}'.format(converted_amount)

    @staticmethod
    def convert_exchange_result_to_model(message:str, amount:float)->ExChangeResultModel:
        return ExChangeResultModel(message=message, amount=amount)
