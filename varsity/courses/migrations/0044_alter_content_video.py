# Generated by Django 4.2.6 on 2024-01-24 08:54

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0043_alter_content_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='video',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='video'),
        ),
    ]
