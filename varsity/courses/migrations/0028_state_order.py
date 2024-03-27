# Generated by Django 4.2.6 on 2024-01-07 00:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_rename_refered_by_mainuser_referred_by'),
        ('courses', '0027_ebook_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('delivery_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False, unique=True)),
                ('address', models.CharField(max_length=250)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.shopproduct')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='courses.state')),
            ],
        ),
    ]