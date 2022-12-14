# Generated by Django 2.2.4 on 2022-09-18 19:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('mobile', models.CharField(blank=True, max_length=50)),
                ('gender', models.CharField(blank=True, max_length=50)),
                ('birth_date', models.DateField(blank=True)),
                ('username', models.SlugField(validators=[django.core.validators.RegexValidator])),
                ('email', models.EmailField(max_length=100, validators=[django.core.validators.EmailValidator])),
                ('password', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator])),
                ('confirmed_pass', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator])),
                ('designation', models.SlugField(validators=[django.core.validators.RegexValidator])),
                ('profile_picture', models.ImageField(blank=True, upload_to='')),
                ('status', models.CharField(default='active', max_length=50, validators=[django.core.validators.RegexValidator])),
                ('trash', models.BooleanField(default=False)),
            ],
        ),
    ]
