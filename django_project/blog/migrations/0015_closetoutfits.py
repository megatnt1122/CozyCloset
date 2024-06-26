# Generated by Django 5.0.1 on 2024-03-24 22:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_closet_is_public_outfit'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='closetOutfits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('closet', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='blog.closet')),
                ('outfit', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='blog.outfit')),
                ('user', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
