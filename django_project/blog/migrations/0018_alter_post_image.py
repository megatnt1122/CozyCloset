# Generated by Django 5.0.1 on 2024-03-06 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default', upload_to='clothing_photos'),
        ),
    ]
