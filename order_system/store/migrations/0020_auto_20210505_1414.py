# Generated by Django 3.1.5 on 2021-05-05 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_auto_20210505_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='invest_balance',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='sav_balance',
        ),
        migrations.AddField(
            model_name='useraccount',
            name='invest_balance',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='sav_balance',
            field=models.FloatField(default=0.0),
        ),
    ]
