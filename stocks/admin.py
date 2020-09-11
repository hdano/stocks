from django.contrib import admin

from .models import Stock, StockOrder, UserStock

admin.site.register(Stock)
admin.site.register(StockOrder)
admin.site.register(UserStock)
