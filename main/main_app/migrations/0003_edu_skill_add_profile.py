# Generated by Django 5.0.3 on 2024-04-03 08:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_add_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edu', models.CharField(max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skil', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Add_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, null=True)),
                ('last_name', models.CharField(max_length=20, null=True)),
                ('email', models.EmailField(max_length=30, null=True)),
                ('mob', models.IntegerField(null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=20, null=True)),
                ('emp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('education', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.edu')),
                ('skills', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.skill')),
            ],
        ),
    ]
