# Generated by Django 4.2.6 on 2023-11-02 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0020_course_what_to_gain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursereview',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='courses.course'),
        ),
    ]
