# Generated by Django 4.2.6 on 2023-10-22 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_remove_course_expectancy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='charge_status',
            field=models.CharField(choices=[('Free', 'Free'), ('Paid', 'Paid')], max_length=4),
        ),
    ]
