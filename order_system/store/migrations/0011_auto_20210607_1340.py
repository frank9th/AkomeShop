# Generated by Django 3.1.5 on 2021-06-07 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20210603_1426'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='seller',
        ),
        migrations.DeleteModel(
            name='FastFood',
        ),
        migrations.DeleteModel(
            name='Food',
        ),
    ]
