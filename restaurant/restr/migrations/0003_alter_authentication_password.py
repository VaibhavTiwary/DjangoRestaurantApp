# Generated by Django 5.0.3 on 2024-03-14 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restr', '0002_authentication_menu_delete_temp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authentication',
            name='password',
            field=models.CharField(max_length=500),
        ),
    ]
