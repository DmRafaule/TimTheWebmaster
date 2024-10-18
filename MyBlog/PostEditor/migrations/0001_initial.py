# Generated by Django 5.1 on 2024-10-18 05:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeCreated', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('template', models.FilePathField(path='C:\\Users\\dima\\Projects\\Web\\TimTheWebmaster\\MyBlog\\media\\tools\\post-editor')),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
                ('filename', models.CharField(max_length=25)),
                ('option', models.IntegerField(choices=[(0, 'Чистый HTML'), (1, 'Для статей'), (2, 'Для определений'), (3, 'Для вопросов')], default=0)),
                ('content', models.TextField(blank=True)),
                ('used_styles', models.TextField(blank=True)),
                ('used_scripts', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
