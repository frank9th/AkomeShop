# Generated by Django 3.1.5 on 2021-08-19 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_transactions_payment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='store_record',
            field=models.BooleanField(default=True),
        ),
    ]
