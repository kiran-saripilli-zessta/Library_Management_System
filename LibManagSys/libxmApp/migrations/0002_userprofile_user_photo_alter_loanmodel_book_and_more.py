# Generated by Django 5.0.1 on 2024-02-02 06:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libxmApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='loanmodel',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='libxmApp.bookmodel'),
        ),
        migrations.AlterField(
            model_name='loanmodel',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='libxmApp.membermodel'),
        ),
    ]
