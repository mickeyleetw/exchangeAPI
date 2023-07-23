from decimal import Decimal
from files.exchange_rate import exchange_rate

from apps.exchange.model import ExChangeResultModel


class ExchangeRepo:
    
    @staticmethod
    def is_source_valid(source:str):
        if source not in exchange_rate['currencies'].keys():
            return False
        return True
    
    @staticmethod
    def is_target_valid(source:str,target:str):
        if target not in exchange_rate['currencies'][source].keys():
            return False
        return True

    @staticmethod
    def convert_currency(source:str, target:str, amount:Decimal ):
        rate = exchange_rate['currencies'][source][target]
        converted_amount = round(float(amount.replace(',', '')) * rate, 2)
        return "{:,.2f}".format(converted_amount)

    @staticmethod
    def convert_exchange_result_to_model(message:str, amount:float):
        return ExChangeResultModel(message=message, amount=amount)
