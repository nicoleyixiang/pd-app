# Generated by Django 3.0.8 on 2021-02-11 01:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0014_auto_20210207_0422'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Customer',
            new_name='Student',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='customer',
            new_name='student',
        ),
    ]
