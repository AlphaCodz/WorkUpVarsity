# Generated by Django 4.2.6 on 2024-01-10 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_recipientholdingaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipientholdingaccount',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL),
        ),
    ]
