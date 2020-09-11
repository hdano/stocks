import json

from django.http import (
    HttpResponse, JsonResponse, Http404
)
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes
)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from .models import Stock, StockOrder, UserStock
from serializers import StockSerializer, StockOrderSerializer


@api_view(['GET'])
@csrf_exempt
def list_stocks(request):
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)
    return JsonResponse(dict(
            data=serializer.data,
            summary=dict(
                    total=Stock.objects.count()
                )
        ), safe=False)


@api_view(['GET'])
@csrf_exempt
def stock_detail(request, pk):
    try:
        stock = Stock.objects.get(pk=pk)
    except Stock.DoesNotExist:
        return JsonResponse(dict(message='Stock #%s does not exist' % pk))
    serializer = StockSerializer(stock)
    return JsonResponse(dict(
            data=serializer.data,
            summary=dict(
                    stock_id=pk
                )
        ), safe=False)


@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def trade_stock(request):
    data = JSONParser().parse(request)
    for field in ['transaction_type', 'stock_id', 'quantity']:
        if field not in data:
            return JsonResponse(dict(
                    message='Missing required field: %s' % field
                ))
    quantity = int(data['quantity'])
    if quantity < 1:
        return JsonResponse(dict(message='Invalid quantity'))
    try:
        stock = Stock.objects.get(pk=data['stock_id'])
    except Stock.DoesNotExist:
        return JsonResponse(dict(message='Item does not exist'))
    transaction_type = data['transaction_type']
    if transaction_type not in ['buy', 'sell']:
        return JsonResponse(dict(
                message=''.join([
                        'Invalid transaction_type. ',
                        'Should be either "buy" or "sell"'
                    ])
            ))
    # Buying
    if transaction_type == 'buy':
        if stock.units_available < 1:
            return JsonResponse(dict(message='Out of stock'))
        elif stock.units_available < quantity:
            return JsonResponse(dict(
                    message='Only %s unit(s) available' % stock.units_available
                ))
    # Selling
    else:
        try:
            user_stock = UserStock.objects.get(user=request.user, stock=stock)
        except UserStock.DoesNotExist:
            return JsonResponse(dict(
                    message='You do not have %s in your inventory' % stock.name
                ))
        if user_stock.total_units < 1:
            return JsonResponse(dict(
                    message='You do not have %s in your inventory' % stock.name
                ))
        elif user_stock.total_units < quantity:
            return JsonResponse(dict(
                    message='You only have %s %s(s) in your inventory' % (
                            user_stock.total_units, stock.name
                        )
                ))
    serializer = StockOrderSerializer(data=data, context={})
    if serializer.is_valid():
        serializer.save()
        order = StockOrder.objects.get(pk=serializer.data['id'])
        # Overrides key values in the stock order row
        order.transaction_type = transaction_type
        order.stock = stock
        order.user = request.user
        order.save()
        # Create/Update user stock records
        try:
            user_stock = UserStock.objects.get(user=request.user, stock=stock)
        except UserStock.DoesNotExist:
            user_stock = UserStock(
                    user=request.user, stock=stock, total_units=0
                )
        multiplier = (1 if transaction_type == 'buy' else -1)
        user_stock.total_units += quantity * multiplier
        user_stock.last_updated = timezone.now()
        user_stock.save()
        # Update units available
        stock.units_available -= quantity * multiplier
        stock.save()
        return JsonResponse(dict(
                message=(''.join([
                        'Thank you for %sing %s %s(s). ',
                        'You now have a total of %s %s(s) ',
                        'in your inventory.']) % (
                                transaction_type,
                                order.quantity,
                                order.stock.name,
                                user_stock.total_units,
                                order.stock.name
                            )
                        )),
                status=201
            )
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def inventory(request):
    data = []
    for user_stock in UserStock.objects.all():
        data.append(dict(
                stock_name=user_stock.stock.name,
                total_units=user_stock.total_units,
                date_added=user_stock.date_added,
                last_updated=user_stock.last_updated,

            ))
    return JsonResponse(dict(data=data), safe=False)


@api_view(['GET'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def inventory_detail(request, pk):
    try:
        stock = Stock.objects.get(pk=pk)
    except Stock.DoesNotExist:
        return JsonResponse(dict(message='Item does not exist'))
    try:
        user_stock = UserStock.objects.get(user=request.user, stock=stock)
    except UserStock.DoesNotExist:
        return JsonResponse(dict(
                message='You do not have %s in your inventory' % stock.name
            ))
    data = dict(
            stock_id=stock.id,
            stock_name=stock.name,
            stock_unit_price=stock.unit_price,
            total_units=user_stock.total_units,
            total_value=(user_stock.total_units * stock.unit_price),
            date_added=user_stock.date_added,
            last_updated=user_stock.last_updated,
        )
    return JsonResponse(dict(data=data), safe=False)
