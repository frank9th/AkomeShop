# Generated by Django 3.1.5 on 2021-05-13 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0035_auto_20210513_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='saving',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
