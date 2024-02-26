# Generated by Django 5.0.1 on 2024-02-01 08:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DemoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('demo_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=200)),
                ('book_unique_isbn', models.CharField(max_length=20, unique=True)),
                ('quantity_available', models.PositiveIntegerField(default=0)),
                ('book_publisher', models.CharField(max_length=150)),
                ('book_author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='libxmApp.author')),
                ('book_genre', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='genre', to='libxmApp.genre')),
            ],
        ),
        migrations.CreateModel(
            name='MemberModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_books_borrowed', models.ManyToManyField(blank=True, related_name='borrowers', to='libxmApp.bookmodel')),
                ('member_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libxmApp.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='LoanModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('return_date', models.DateField(blank=True, null=True)),
                ('fine', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('loan_status', models.CharField(max_length=20)),
                ('loan_date', models.DateField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libxmApp.bookmodel')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libxmApp.membermodel')),
            ],
        ),
    ]
