# Generated by Django 4.2.6 on 2024-01-08 00:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_rename_refered_by_mainuser_referred_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipientAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=12, unique=True)),
                ('name', models.CharField(max_length=300)),
                ('bank_code', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]