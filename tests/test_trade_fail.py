import json

import pytest
from django.contrib.auth.models import User

from stocks.models import Stock, UserStock


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_unauthorized(api_client):
    """
    Unauthorized access.
    """
    url = '/stocks/trade/'
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_invalid_method(api_client, get_or_create_token):
    """
    Invalid method GET
    """
    url = '/stocks/trade/'
    api_client.credentials(HTTP_AUTHORIZATION='Token %s' % get_or_create_token)
    response = api_client.get(url)
    assert response.status_code == 405


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_missing_request_data(api_client, get_or_create_token):
    """
    Request data are missing.
    """
    url = '/stocks/trade/'
    api_client.credentials(HTTP_AUTHORIZATION='Token %s' % get_or_create_token)
    response = api_client.post(url, '{}', content_type="application/json")
    assert response.status_code == 200
    rjson = response.json()
    assert rjson['message'][:22] == 'Missing required field'


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_missing_request_data(api_client, get_or_create_token):
    """
    Request data are missing.
    """
    url = '/stocks/trade/'
    api_client.credentials(HTTP_AUTHORIZATION='Token %s' % get_or_create_token)
    response = api_client.post(url, '{}', content_type="application/json")
    assert response.status_code == 200
    rjson = response.json()
    assert rjson['message'][:22] == 'Missing required field'


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_invalid_quantity(api_client, get_or_create_token):
    """
    Quantity is invalid
    """
    # setup sample stock
    starting_units_available = 100
    apple = Stock(
            name='Apple', unit_price=5.00,
            units_available=starting_units_available
        )
    apple.save()
    # build request json data
    data = dict(
            transaction_type='buy',
            stock_id=apple.id,
            quantity=0
        )
    # call endpoint
    url = '/stocks/trade/'
    api_client.credentials(HTTP_AUTHORIZATION='Token %s' % get_or_create_token)
    response = api_client.post(
            url, json.dumps(data), content_type="application/json"
        )
    # test response
    assert response.status_code == 200
    rjson = response.json()
    assert rjson['message'] == 'Invalid quantity'


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_nonexisting_stock_id(api_client, get_or_create_token):
    """
    stock_id is nonexisting.
    """
    # build request json data
    data = dict(
            transaction_type='buy',
            stock_id=999999,
            quantity=5
        )
    # call endpoint
    url = '/stocks/trade/'
    api_client.credentials(HTTP_AUTHORIZATION='Token %s' % get_or_create_token)
    response = api_client.post(
            url, json.dumps(data), content_type="application/json"
        )
    # test response
    assert response.status_code == 200
    rjson = response.json()
    assert rjson['message'] == 'Item does not exist'


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_invalid_transaction(api_client, get_or_create_token):
    """
    Invalid transaction, should be "buy" or "sell".
    """
    # setup sample stock
    starting_units_available = 100
    apple = Stock(
            name='Apple', unit_price=5.00,
            units_available=starting_units_available
        )
    apple.save()
    # build request json data
    data = dict(
            transaction_type='steal',
            stock_id=apple.id,
            quantity=5
        )
    # call endpoint
    url = '/stocks/trade/'
    api_client.credentials(HTTP_AUTHORIZATION='Token %s' % get_or_create_token)
    response = api_client.post(
            url, json.dumps(data), content_type="application/json"
        )
    # test response
    assert response.status_code == 200
    rjson = response.json()
    assert rjson['message'][:25] == 'Invalid transaction_type.'


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_buy_outofstock(api_client, get_or_create_token):
    """
    Buying, out of stock.
    """
    # setup sample stock
    starting_units_available = 0
    apple = Stock(
            name='Apple', unit_price=5.00,
            units_available=starting_units_available
        )
    apple.save()
    # build request json data
    data = dict(
            transaction_type='buy',
            stock_id=apple.id,
            quantity=5
        )
    # call endpoint
    url = '/stocks/trade/'
    api_client.credentials(HTTP_AUTHORIZATION='Token %s' % get_or_create_token)
    response = api_client.post(
            url, json.dumps(data), content_type="application/json"
        )
    # test response
    assert response.status_code == 200
    rjson = response.json()
    assert rjson['message'] == 'Out of stock'


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_buy_insufficient_stock(api_client, get_or_create_token):
    """
    Buying, insufficient stock.
    """
    # setup sample stock
    starting_units_available = 4
    apple = Stock(
            name='Apple', unit_price=5.00,
            units_available=starting_units_available
        )
    apple.save()
    # build request json data
    data = dict(
            transaction_type='buy',
            stock_id=apple.id,
            quantity=5
        )
    # call endpoint
    url = '/stocks/trade/'
    api_client.credentials(HTTP_AUTHORIZATION='Token %s' % get_or_create_token)
    response = api_client.post(
            url, json.dumps(data), content_type="application/json"
        )
    # test response
    assert response.status_code == 200
    rjson = response.json()
    assert rjson['message'] == 'Only %s unit(s) available' % (
            starting_units_available
        )


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_sell_no_stock(api_client, get_or_create_token):
    """
    Selling, stock not available in inventory.
    """
    # setup sample stock and inventory
    apple = Stock(
            name='Apple', unit_price=5.00,
            units_available=100
        )
    apple.save()
    # build request json data
    data = dict(
            transaction_type='sell',
            stock_id=apple.id,
            quantity=5
        )
    # call endpoint
    url = '/stocks/trade/'
    api_client.credentials(HTTP_AUTHORIZATION='Token %s' % get_or_create_token)
    response = api_client.post(
            url, json.dumps(data), content_type="application/json"
        )
    # test response
    assert response.status_code == 200
    rjson = response.json()
    assert rjson['message'] == 'You do not have %s in your inventory' % (
            apple.name
        )


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_sell_empty_stock(api_client, get_or_create_token):
    """
    Selling, stock is empty in inventory.
    """
    # setup sample stock and inventory
    apple = Stock(
            name='Apple', unit_price=5.00,
            units_available=100
        )
    apple.save()
    user = User.objects.get(username='user1')
    user_stock = UserStock(user=user, stock=apple, total_units=0)
    user_stock.save()
    # build request json data
    data = dict(
            transaction_type='sell',
            stock_id=apple.id,
            quantity=5
        )
    # call endpoint
    url = '/stocks/trade/'
    api_client.credentials(HTTP_AUTHORIZATION='Token %s' % get_or_create_token)
    response = api_client.post(
            url, json.dumps(data), content_type="application/json"
        )
    # test response
    assert response.status_code == 200
    rjson = response.json()
    assert rjson['message'] == 'You do not have %s in your inventory' % (
            apple.name
        )


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_sell_insufficient_inventory(
            api_client, get_or_create_token
        ):
    """
    Selling, insufficient inventory.
    """
    # setup sample stock and inventory
    apple = Stock(
            name='Apple', unit_price=5.00,
            units_available=100
        )
    apple.save()
    user = User.objects.get(username='user1')
    user_stock = UserStock(user=user, stock=apple, total_units=4)
    user_stock.save()
    # build request json data
    data = dict(
            transaction_type='sell',
            stock_id=apple.id,
            quantity=5
        )
    # call endpoint
    url = '/stocks/trade/'
    api_client.credentials(HTTP_AUTHORIZATION='Token %s' % get_or_create_token)
    response = api_client.post(
            url, json.dumps(data), content_type="application/json"
        )
    # test response
    assert response.status_code == 200
    rjson = response.json()
    assert rjson['message'] == 'You only have %s %s(s) in your inventory' % (
            user_stock.total_units,
            apple.name
        )
