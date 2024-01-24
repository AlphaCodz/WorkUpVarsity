# Generated by Django 4.2.6 on 2024-01-24 08:15

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0042_alter_content_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='video',
            field=models.FileField(storage=cloudinary_storage.storage.VideoMediaCloudinaryStorage, upload_to='course-videos'),
        ),
    ]
