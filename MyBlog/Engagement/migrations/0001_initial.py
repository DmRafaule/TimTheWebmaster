# Generated by Django 5.1 on 2024-12-19 06:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=512)),
                ('views', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('shares', models.IntegerField(default=0)),
                ('comments', models.IntegerField(default=0)),
                ('bookmarks', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_published', models.DateTimeField(auto_created=True, auto_now=True)),
                ('url', models.CharField(max_length=512)),
                ('name', models.CharField(max_length=20)),
                ('message', models.TextField(max_length=1024)),
                ('interaction', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Engagement.interaction')),
            ],
        ),
    ]
