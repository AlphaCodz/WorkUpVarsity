# Generated by Django 4.2.6 on 2023-12-30 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_mainuser_status_shopproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainuser',
            name='affiliate_code',
            field=models.CharField(max_length=7, null=True, unique=True),
        ),
    ]