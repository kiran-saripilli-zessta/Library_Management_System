# Generated by Django 5.0.1 on 2024-02-21 09:55

import libxmApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libxmApp', '0010_alter_userprofile_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_photo',
            field=models.ImageField(storage=libxmApp.models.S3MediaStorage(), upload_to='media'),
        ),
    ]
