# Generated by Django 5.1 on 2024-08-26 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0004_delete_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='categry_name',
            field=models.SlugField(blank=True, default='', null=True),
        ),
    ]
