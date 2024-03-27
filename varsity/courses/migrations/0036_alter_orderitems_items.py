# Generated by Django 4.2.6 on 2024-01-07 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_rename_refered_by_mainuser_referred_by'),
        ('courses', '0035_orderitems_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='items',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item', to='main_app.shopproduct'),
        ),
    ]