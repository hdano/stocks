# Generated by Django 3.1.1 on 2020-09-03 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_auto_20200904_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockorder',
            name='status',
            field=models.CharField(default='completed', max_length=15),
        ),
        migrations.AlterField(
            model_name='stockorder',
            name='date_completed',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
