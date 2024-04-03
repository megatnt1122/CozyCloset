# Generated by Django 5.0.1 on 2024-03-24 02:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_closet_is_public'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='closet',
            name='is_public',
            field=models.BooleanField(default=True, verbose_name='Public'),
        ),
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accessory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Accessory', to='blog.userclothes')),
                ('bottoms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Bottoms', to='blog.userclothes')),
                ('footwear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Footwear', to='blog.userclothes')),
                ('outerwear', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Outerwear', to='blog.userclothes')),
                ('top', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Top', to='blog.userclothes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
