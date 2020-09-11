# Stocks Trade API App

This is a simple Python/Django demo app coded by Harrison Dano to demonstrate Python and Django skills.

## Requirements

Please build a simple trading system as a pure REST API with the endpoints outlined below. We want to allow authenticated users the ability to place orders to buy and sell stocks and track the overall value of their investments. Stocks will have an id, name, and price. 

- Create an endpoint to let users place trades. When an order is placed we need to record the quantity of the stock the user wants to buy or sell. 
- Create an endpoint to retrieve the total value invested in a single stock by a user. To calculate this - we need to sum all the value of all orders placed by the user for a single stock. Order value is calculated by multiplying quantity and stock price. 
- Create an endpoint to retrieve the total value invested in a single stock by a user. 

## Running App

Create virtual environment and install packages


```bash
virtualenv -p python3 .env
source .env/bin/activate
pip install -r requirements.txt
```

Build sqlite database and create superuser


```bash
python manage.py migrate
python manage.py createsuperuser
```

Create user token and write it down for later use

```bash
python manage.py shell

(InteractiveConsole)
>>> from stocks.models import User
>>> user = User.objects.get(username=...)
>>> from rest_framework.authtoken.models import Token
>>> token, created = Token.objects.get_or_create(user=user)
>>> token
<Token ...>
>>> exit()
```

Create sample stocks


```bash
python manage.py shell

(InteractiveConsole)
>>> from stocks.models import Stock
>>> apple = Stock(name='Apple', unit_price=5.00, units_available=100)
>>> apple.save()
>>> banana = Stock(name='banana', unit_price=7.00, units_available=100)
>>> banana.save()
>>> exit()
```

Run app

```bash
python manage.py runserver
```

## Buying Stocks

Using cURL, for example, buying 5 apples

```bash
curl -H "Authorization: Token ..." -X POST http://localhost:8000/stocks/trade/ -d '{"transaction_type": "buy", "stock_id": 1, "quantity": 5}' -H "Content-Type: application/json"

{"message": "Thank you for buying 5 Apple(s). You now have a total of 5 Apple(s) in your inventory."}
```

## Selling Stocks

Using cURL, for example, selling 5 apples

```bash
curl -H "Authorization: Token ..." -X POST http://localhost:8000/stocks/trade/ -d '{"transaction_type": "sell", "stock_id": 1, "quantity": 5}' -H "Content-Type: application/json"

{"message": "Thank you for selling 5 Apple(s). You now have a total of 0 Apple(s) in your inventory."}
```

## Getting all stocks in inventory

This will display all stocks you purchased and currently in your inventory


```bash
curl -H "Authorization: Token ..." http://localhost:8000/stocks/inventory/ -H "Content-Type: application/json" 

{"data": [{"stock_name": "Apple", "total_units": 22, "date_added": "2020-09-03T17:18:17.174Z", "last_updated": "2020-09-04T18:26:59.613Z"}, {"stock_name": "Banana", "total_units": 45, "date_added": "2020-09-03T17:19:38.548Z", "last_updated": "2020-09-04T16:19:54.759Z"}]}
```	

## Getting information about a stock in your inventory

By providing the stock id (e.g. `1`) in the endpoint, this will display information about that stock including the total investment value named as `total_value`


```bash
curl -H "Authorization: Token ..." http://localhost:8000/stocks/inventory/1/ -H "Content-Type: application/json"

{"data": {"stock_id": 1, "stock_name": "Apple", "stock_unit_price": "5.00", "total_units": 22, "total_value": "110.00", "date_added": "2020-09-03T17:18:17.174Z", "last_updated": "2020-09-04T18:26:59.613Z"}}
```	

## Testing

### Unit Test

Unit test files are located in `/tests/`

```bash
pytest -vv
```
