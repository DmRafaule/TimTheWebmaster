# Generated by Django 5.1 on 2025-02-28 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0026_alter_tool_default_template'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qa',
            name='default_template',
        ),
        migrations.RemoveField(
            model_name='qa',
            name='template',
        ),
        migrations.RemoveField(
            model_name='qa',
            name='template_en',
        ),
        migrations.RemoveField(
            model_name='qa',
            name='template_ru',
        ),
        migrations.RemoveField(
            model_name='td',
            name='default_template',
        ),
        migrations.RemoveField(
            model_name='td',
            name='template',
        ),
        migrations.RemoveField(
            model_name='td',
            name='template_en',
        ),
        migrations.RemoveField(
            model_name='td',
            name='template_ru',
        ),
    ]
