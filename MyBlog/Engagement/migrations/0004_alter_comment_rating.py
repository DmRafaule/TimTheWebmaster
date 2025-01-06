# Generated by Django 5.1 on 2025-01-06 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Engagement', '0003_comment_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five'), (0, 'Zero')], default=0),
        ),
    ]
