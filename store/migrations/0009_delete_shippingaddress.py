# Generated by Django 3.0.8 on 2021-01-29 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_category_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShippingAddress',
        ),
    ]
