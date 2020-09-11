from rest_framework import serializers
from stocks.models import Stock, StockOrder
from django.utils import timezone


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'name', 'unit_price', 'units_available']


class StockOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    # either 'buy' or 'sell'
    transaction_type = serializers.CharField(max_length=15)
    stock_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=0)
    date_ordered = serializers.DateTimeField(read_only=True, required=False)
    # To simplify the app, status will be "completed" by default
    # so all transactions are reflected automatically
    status = serializers.CharField(
        read_only=True, max_length=15, default='completed')
    date_completed = serializers.DateTimeField(read_only=True, required=False)

    def create(self, validated_data):
        return StockOrder.objects.create(**validated_data)
