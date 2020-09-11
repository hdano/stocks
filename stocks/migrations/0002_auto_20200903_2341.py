# Generated by Django 3.1.1 on 2020-09-03 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='stock_id',
        ),
        migrations.AlterField(
            model_name='stockorder',
            name='date_completed',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='stockorder',
            name='date_ordered',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='stockorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),  # noqa
        ),
        migrations.AlterField(
            model_name='userstock',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),  # noqa
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]