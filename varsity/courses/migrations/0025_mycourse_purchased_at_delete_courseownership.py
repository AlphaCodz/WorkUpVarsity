# Generated by Django 4.2.6 on 2024-01-03 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0024_mycourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycourse',
            name='purchased_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.DeleteModel(
            name='CourseOwnership',
        ),
    ]
