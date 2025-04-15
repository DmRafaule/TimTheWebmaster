# Generated by Django 5.1 on 2025-04-15 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0021_alter_website_articles_post_preview_and_more'),
        ('Post', '0030_post_media_tool_similar_alter_platform_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='similar',
            field=models.ManyToManyField(blank=True, help_text='Up to 3 choises', to='Post.article'),
        ),
        migrations.AlterField(
            model_name='post',
            name='media',
            field=models.ManyToManyField(blank=True, help_text='Will be procceed only First ones added video, pdf, audio files. On Tool model audio and pdf files has no effect.', to='Main.media'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='similar',
            field=models.ManyToManyField(blank=True, help_text='Up to 3 choises', to='Post.tool'),
        ),
    ]
