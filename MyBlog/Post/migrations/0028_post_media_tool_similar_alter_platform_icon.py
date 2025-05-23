# Generated by Django 5.1 on 2025-04-14 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0021_alter_website_articles_post_preview_and_more'),
        ('Post', '0027_remove_post_similar_article_similar'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='media',
            field=models.ManyToManyField(blank=True, to='Main.media'),
        ),
        migrations.AddField(
            model_name='tool',
            name='similar',
            field=models.ManyToManyField(blank=True, to='Post.tool'),
        ),
        migrations.AlterField(
            model_name='platform',
            name='icon',
            field=models.FileField(upload_to='common'),
        ),
    ]
