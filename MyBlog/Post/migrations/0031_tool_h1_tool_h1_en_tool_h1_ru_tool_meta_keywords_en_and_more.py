# Generated by Django 5.1 on 2025-05-14 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0030_tool_meta_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='h1',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='tool',
            name='h1_en',
            field=models.CharField(default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tool',
            name='h1_ru',
            field=models.CharField(default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tool',
            name='meta_keywords_en',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tool',
            name='meta_keywords_ru',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
    ]
