# Generated by Django 4.2.6 on 2024-01-15 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_alter_recipientholdingaccount_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipientholdingaccount',
            name='bank_code',
            field=models.CharField(max_length=7, null=True),
        ),
    ]
