# Generated by Django 5.0.3 on 2024-03-18 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restr', '0004_authentication_username'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Authentication',
        ),
    ]