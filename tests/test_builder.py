from unittest.mock import Mock

import pytest

from bnc.builder import Builder

SIGNATURE = 'SIGNATURE'
API_KEY = 'API_KEY'
RESPONSE_OBJ = {'key': 1}


@pytest.fixture
def mocked_deps(mocker):
    mocker.patch('bnc.builder.get_hmac_hash', return_value=SIGNATURE)
    mocker.patch('bnc.builder.get_secret_key', return_value='MY_SECRET_KEY')
    mocker.patch('bnc.builder.read_configuration', return_value={'is_testnet': False,
                                                                 'bnc_api_endpoint': 'BINANCE_URL'})
    mocker.patch('bnc.builder.get_api_key_header', return_value={'X-MBX-APIKEY': API_KEY})
    mocker.patch('bnc.builder.to_query_string_parameters', return_value='KEY=VALUE&KEY1=VALUE1')

    mock_response = Mock(status_code=200)
    mock_response.json.return_value = RESPONSE_OBJ

    mocker.patch('bnc.builder.requests.get', return_value=mock_response)


def test_builder_default_method_is_get(mocked_deps):
    builder = Builder(endpoint='/test', payload={'key': 1})
    assert builder.method == 'GET'


@pytest.mark.parametrize("values", [None, ''])
def test_builder_endpoint_is_null_or_empty(values):
    with pytest.raises(ValueError, match='endpoint cannot be null or empty'):
        Builder(endpoint=values, payload={})


def test_builder_change_method_is_post(mocked_deps):
    builder = Builder(endpoint='/test', payload={'key': 1}, method='POST')
    assert builder.method == 'POST'


def test_builder_incorrect_method():
    with pytest.raises(ValueError, match='Http method is invalid'):
        Builder(endpoint='/test', payload={'key': 1}, method='TEST')


def test_set_security_payload_and_headers_ok(mocked_deps):
    builder = Builder(endpoint='/test', payload={'key': 1}).set_security()

    assert 'signature' in builder.payload
    assert builder.payload['signature'] == SIGNATURE

    assert 'X-MBX-APIKEY' in builder.headers
    assert builder.headers['X-MBX-APIKEY'] == API_KEY


@pytest.mark.asyncio
async def test_send_http_req_ok(mocked_deps):
    builder = Builder(endpoint='/test', payload={'key': 1}).set_security()
    await builder.send_http_req()

    assert builder.response.status_code == 200
    assert builder.response.json() == RESPONSE_OBJ


@pytest.mark.asyncio
async def test_handle_response_200_ok(mocked_deps):
    builder = Builder(endpoint='/test', payload={'key': 1}).set_security()
    await builder.send_http_req()

    builder.handle_response()

    assert not builder.has_error
    assert dict(builder.result)
    assert builder.result['successful'] == True
    assert builder.result['status_code'] == 200
    assert builder.result['results'] == RESPONSE_OBJ
