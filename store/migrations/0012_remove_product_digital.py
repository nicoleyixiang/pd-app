# Generated by Django 3.0.8 on 2021-02-02 03:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_remove_product_diameter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
    ]
