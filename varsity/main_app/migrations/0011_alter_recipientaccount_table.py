# Generated by Django 4.2.6 on 2024-01-10 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_recipientaccount'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='recipientaccount',
            table='main_app_recipientaccount',
        ),
    ]