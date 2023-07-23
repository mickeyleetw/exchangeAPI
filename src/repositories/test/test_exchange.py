import pytest
from core.enum import CurrencyEnum
from core.exception import ResourceNotFoundException

from repositories.exchange import ExchangeRepo


def test_is_source_valid(exchange_map):

    is_source_valid = ExchangeRepo.is_source_valid(source_currency=CurrencyEnum.JPY,exchange_map=exchange_map)
    assert is_source_valid is True
    
    is_source_valid = ExchangeRepo.is_source_valid(source_currency=CurrencyEnum.USD,exchange_map=exchange_map)
    assert is_source_valid is False


def test_is_target_valid(exchange_map):

    is_target_valid = ExchangeRepo.is_target_valid(source_currency=CurrencyEnum.JPY,target_currency=CurrencyEnum.TWD,exchange_map=exchange_map)
    assert is_target_valid is True

    is_target_valid = ExchangeRepo.is_target_valid(source_currency=CurrencyEnum.JPY,target_currency=CurrencyEnum.USD,exchange_map=exchange_map)
    assert is_target_valid is False


def test_convert_currency(exchange_map):
    converted_amount=ExchangeRepo.convert_currency(source_currency=CurrencyEnum.TWD,target_currency=CurrencyEnum.JPY,amount='$1,000',exchange_map=exchange_map)
    assert converted_amount=='$4,000.00'
    
    with pytest.raises(ResourceNotFoundException):
        ExchangeRepo.convert_currency(source_currency=CurrencyEnum.TWD,target_currency=CurrencyEnum.USD,amount='$1,000',exchange_map=exchange_map)
        