# Generated by Django 5.2 on 2025-05-21 07:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_profile_avatar_alter_video_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=255)),
                ('searched_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
