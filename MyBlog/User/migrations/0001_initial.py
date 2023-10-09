# Generated by Django 4.2.5 on 2023-10-09 09:59

import Post.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256)),
                ('content', models.TextField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('slug', models.SlugField(max_length=256, unique=True)),
                ('about', models.TextField(blank=True)),
                ('avatar', models.ImageField(blank=True, upload_to=Post.models.user_directory_path)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('tags', models.ManyToManyField(blank=True, to='Post.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('forAll', models.BooleanField(default=False)),
                ('tags', models.ManyToManyField(blank=True, to='Post.tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timeCreated', models.DateTimeField(auto_now_add=True)),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
                ('tags', models.ManyToManyField(blank=True, to='Post.tag')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Post.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.user')),
            ],
        ),
    ]
