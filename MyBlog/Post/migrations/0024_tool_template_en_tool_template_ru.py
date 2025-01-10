# Generated by Django 5.1 on 2025-01-10 14:37

import Post.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0023_tool_price_tool_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='template_en',
            field=models.FileField(blank=True, help_text='If provided, default template not in use. Use only if it is Internal default type', max_length=300, null=True, upload_to=Post.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='tool',
            name='template_ru',
            field=models.FileField(blank=True, help_text='If provided, default template not in use. Use only if it is Internal default type', max_length=300, null=True, upload_to=Post.models.user_directory_path),
        ),
    ]
