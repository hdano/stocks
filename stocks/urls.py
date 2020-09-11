from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_stocks, name='list-stocks'),
    path('detail/<str:pk>/', views.stock_detail, name='stock-detail'),
    path('trade/', views.trade_stock, name='trade-stock'),
    path('inventory/', views.inventory, name='inventory'),
    path(
            'inventory/<str:pk>/',
            views.inventory_detail,
            name='inventory-detail'
        ),
]
