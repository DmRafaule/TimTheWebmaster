# Generated by Django 5.1 on 2024-08-30 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0006_alter_image_tags'),
        ('Post', '0005_category_categry_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='+', to='Post.tag'),
        ),
    ]
