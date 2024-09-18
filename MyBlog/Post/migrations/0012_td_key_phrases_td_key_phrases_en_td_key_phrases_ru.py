# Generated by Django 5.1 on 2024-09-16 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0011_remove_news_post_ptr_delete_case_delete_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='td',
            name='key_phrases',
            field=models.CharField(blank=True, help_text='To be used to search place for inserting a link. Use , as separator.', max_length=254),
        ),
        migrations.AddField(
            model_name='td',
            name='key_phrases_en',
            field=models.CharField(blank=True, help_text='To be used to search place for inserting a link. Use , as separator.', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='td',
            name='key_phrases_ru',
            field=models.CharField(blank=True, help_text='To be used to search place for inserting a link. Use , as separator.', max_length=254, null=True),
        ),
    ]