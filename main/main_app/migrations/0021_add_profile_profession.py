# Generated by Django 5.0.3 on 2024-04-27 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0020_alter_add_job_education_alter_add_job_skill'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_profile',
            name='profession',
            field=models.CharField(max_length=20, null=True),
        ),
    ]