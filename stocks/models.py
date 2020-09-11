from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Stock(models.Model):
    # stock_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    units_available = models.IntegerField(default=0)

    def __str__(self):
        return "#%s: %s (%s)" % (self.id, self.name, self.units_available)


class StockOrder(models.Model):
    # either 'buy' or 'sell'
    transaction_type = models.CharField(max_length=15, default='buy')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    # To simplify the app, status will be "completed" by default
    # so all transactions are reflected automatically
    # either 'pending', 'completed', 'cancelled'
    status = models.CharField(max_length=15, default='completed')
    date_completed = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "#%s: %s %ss %s %s(s)" % (
                self.id,
                self.user.username if self.user is not None else 'unknown',
                self.transaction_type,
                self.quantity,
                self.stock.name
            )


class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    total_units = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "#%s %s has %s %s(s)" % (
                self.id,
                self.user.username if self.user is not None else 'unknown',
                self.total_units,
                self.stock.name
            )
