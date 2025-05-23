# Generated by Django 5.1 on 2025-05-07 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Engagement', '0005_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_root',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='replies',
            field=models.ManyToManyField(blank=True, to='Engagement.comment'),
        ),
    ]
