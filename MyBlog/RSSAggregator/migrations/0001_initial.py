# Generated by Django 5.0.3 on 2024-03-10 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100, null=True)),
                ('group', models.CharField(blank=True, max_length=256)),
                ('source', models.URLField()),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
