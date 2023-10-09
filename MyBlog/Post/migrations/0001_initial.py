# Generated by Django 4.2.5 on 2023-10-09 09:59

import Post.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('name_ru', models.CharField(max_length=256, null=True)),
                ('name_en', models.CharField(max_length=256, null=True)),
                ('type', models.CharField(max_length=50)),
                ('short_description', models.TextField(blank=True)),
                ('short_description_ru', models.TextField(blank=True, null=True)),
                ('short_description_en', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=256, unique=True)),
                ('timeCreated', models.DateTimeField(auto_now_add=True)),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
                ('isPublished', models.BooleanField(default=True)),
                ('preview', models.ImageField(blank=True, upload_to=Post.models.user_directory_path)),
                ('template', models.FileField(upload_to=Post.models.user_directory_path)),
                ('template_ru', models.FileField(null=True, upload_to=Post.models.user_directory_path)),
                ('template_en', models.FileField(null=True, upload_to=Post.models.user_directory_path)),
                ('likes', models.IntegerField(default=0)),
                ('shares', models.IntegerField(default=0)),
                ('viewed', models.IntegerField(default=0)),
                ('tags', models.ManyToManyField(blank=True, to='Post.tag')),
            ],
        ),
    ]
