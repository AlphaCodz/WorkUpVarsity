# Generated by Django 4.2.6 on 2024-01-07 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0029_order_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='created_at',
        ),
    ]
