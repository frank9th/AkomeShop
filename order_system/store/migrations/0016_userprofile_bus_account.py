# Generated by Django 3.1.5 on 2021-04-23 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staffs', '0012_auto_20210423_1711'),
        ('store', '0015_userprofile_wallet_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bus_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='staffs.vendor'),
        ),
    ]
