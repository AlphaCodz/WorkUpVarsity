# Generated by Django 4.2.6 on 2023-11-01 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_question_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='text',
            field=models.TextField(null=True),
        ),
    ]