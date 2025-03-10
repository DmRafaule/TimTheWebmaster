# Generated by Django 5.1 on 2024-12-09 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0013_rename_default_icon_preview_website_notes_post_preview'),
        ('Post', '0018_alter_note_description_alter_note_description_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='choosen_tools',
            field=models.ManyToManyField(blank=True, related_name='choosen_tools', to='Post.tool', verbose_name='Tools to display at home page'),
        ),
    ]
