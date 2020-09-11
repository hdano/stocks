# Generated by Django 3.1.1 on 2020-09-03 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # noqa
                ('stock_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=8)),  # noqa
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # noqa
                ('token', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # noqa
                ('total_units', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stock')),  # noqa
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.user')),  # noqa
            ],
        ),
        migrations.CreateModel(
            name='StockOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # noqa
                ('order_type', models.CharField(max_length=15)),
                ('quantity', models.IntegerField(default=0)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('date_completed', models.DateTimeField()),
                ('status', models.CharField(default='pending', max_length=15)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stock')),  # noqa
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.user')),  # noqa
            ],
        ),
    ]