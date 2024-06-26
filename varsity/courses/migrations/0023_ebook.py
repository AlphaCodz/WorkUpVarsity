# Generated by Django 4.2.6 on 2023-12-28 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0022_content_content_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='ebooks')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
            ],
        ),
    ]
