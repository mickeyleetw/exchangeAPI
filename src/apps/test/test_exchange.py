import pytest
from core.enum import CurrencyEnum,ErrorCode
from core.exception import ResourceNotFoundException
from starlette import status

from repositories.exchange import ExchangeRepo

mock_exchange_rate ={
    "currencies": {
        "TWD": {
            "TWD": 1,
            "JPY": 4
        },
        "JPY": {
            "TWD": 0.25,
            "JPY": 1
        }
    }
}

@pytest.mark.anyio
async def test_currency_exchange(client):
    
    query_filter = {'source':CurrencyEnum.TWD.value,'target':CurrencyEnum.JPY.value,'amount':'$1,000' }
    response = await client.get('/exchanges', params=query_filter)
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    assert response_data['message']=='success'
    assert response_data['amount']=='$4,000.00'
    
    query_filter = {'target':CurrencyEnum.JPY.value,'amount':'$1,000' }
    response = await client.get('/exchanges', params=query_filter)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    response_data = response.json()
    assert response_data['code']== ErrorCode.GENERAL_1002_REQUEST_VALIDATION_FAILED

    query_filter = {'source':CurrencyEnum.JPY.value,'amount':'$1,000' }
    response = await client.get('/exchanges', params=query_filter)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    response_data = response.json()
    assert response_data['code']== ErrorCode.GENERAL_1002_REQUEST_VALIDATION_FAILED
    
    query_filter = {'source':CurrencyEnum.JPY.value,'target':CurrencyEnum.JPY.value}
    response = await client.get('/exchanges', params=query_filter)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    response_data = response.json()
    assert response_data['code']== ErrorCode.GENERAL_1002_REQUEST_VALIDATION_FAILED
    
    query_filter = {'source':CurrencyEnum.USD.value,'target':CurrencyEnum.JPY.value,'amount':'$1,000'}
    response = await client.get('/exchanges', params=query_filter)
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    response_data = response.json()
    assert response_data['code']== ErrorCode.RESOURCE_2001_NOT_FOUND
    assert response_data['message']=='Source Currency not found'
    
    query_filter = {'source':CurrencyEnum.TWD.value,'target':CurrencyEnum.USD.value,'amount':'$1,000'}
    response = await client.get('/exchanges', params=query_filter)
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    response_data = response.json()
    assert response_data['code']== ErrorCode.RESOURCE_2001_NOT_FOUND
    assert response_data['message']=='Source and Target Currency relation not found'
