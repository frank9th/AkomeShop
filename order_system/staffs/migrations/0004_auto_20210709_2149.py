# Generated by Django 3.1.5 on 2021-07-09 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20210709_2149'),
        ('staffs', '0003_expensis'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Vendor',
            new_name='Seller',
        ),
        migrations.DeleteModel(
            name='Expensis',
        ),
    ]
