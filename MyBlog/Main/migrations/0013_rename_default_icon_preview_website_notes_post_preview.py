# Generated by Django 5.1 on 2024-12-08 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0012_website_default_icon_preview_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='website',
            old_name='default_icon_preview',
            new_name='notes_post_preview',
        ),
    ]
