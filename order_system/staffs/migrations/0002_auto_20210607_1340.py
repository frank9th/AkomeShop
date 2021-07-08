# Generated by Django 3.1.5 on 2021-06-07 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='description',
            field=models.TextField(default=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendor',
            name='fast_food',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vendor',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product'),
        ),
    ]
