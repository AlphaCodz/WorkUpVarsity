# Generated by Django 4.2.6 on 2023-10-15 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_mainuser_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainuser',
            name='city',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='mainuser',
            name='contact',
            field=models.CharField(max_length=11, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='mainuser',
            name='country',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='mainuser',
            name='linkedin_profile',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='mainuser',
            name='state',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='mainuser',
            name='street_address',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='mainuser',
            name='title',
            field=models.CharField(choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs.')], max_length=4, null=True),
        ),
    ]
