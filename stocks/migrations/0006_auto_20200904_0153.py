# Generated by Django 3.1.1 on 2020-09-03 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0005_auto_20200904_0023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockorder',
            old_name='order_type',
            new_name='transaction_type',
        ),
    ]
