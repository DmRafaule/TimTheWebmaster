# Generated by Django 5.1 on 2024-08-30 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0004_category_categry_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
