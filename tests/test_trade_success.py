import json

import pytest
from django.contrib.auth.models import User

from stocks.models import Stock, UserStock


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_buy(api_client, get_or_create_token):
    """
    Buy stocks.
    """
    # setup sample stock
    starting_units_available = 100
    apple = Stock(
            name='Apple', unit_price=5.00,
            units_available=starting_units_available
        )
    apple.save()
    # make sure user doesn't have this stock yet in inventory
    with pytest.raises(UserStock.DoesNotExist):
        _ = UserStock.objects.get(stock=apple)
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
    assert response.status_code == 201
    rjson = response.json()
    assert rjson['message'][:9] == 'Thank you'
    # test product inventory
    user = User.objects.get(username='user1')
    user_stock = UserStock.objects.get(user=user, stock=apple)
    assert user_stock.total_units == data['quantity']
    # test available stock units
    apple = Stock.objects.get(name='Apple')
    assert apple.units_available == starting_units_available - data['quantity']


@pytest.mark.django_db(transaction=True)
def test_stocks_trade_sell(api_client, get_or_create_token):
    """
    Sell stocks.
    """
    # setup sample stock
    starting_units_available = 100
    apple = Stock(
            name='Apple', unit_price=5.00,
            units_available=starting_units_available
        )
    apple.save()
    user = User.objects.get(username='user1')
    starting_total_units = 17
    user_stock = UserStock(
            user=user, stock=apple, total_units=starting_total_units
        )
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
    assert response.status_code == 201
    rjson = response.json()
    assert rjson['message'][:9] == 'Thank you'
    # test product inventory
    user_stock = UserStock.objects.get(user=user, stock=apple)
    assert user_stock.total_units == starting_total_units - data['quantity']
    # test available stock units
    apple = Stock.objects.get(name='Apple')
    assert apple.units_available == starting_units_available + data['quantity']
