# Generated by Django 5.0.1 on 2024-01-12 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_clothingcategories_clothingstyles_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.RemoveField(
            model_name='userclothes',
            name='userID',
        ),
        migrations.RemoveField(
            model_name='userclothes',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='userclothes',
            name='clothingID',
        ),
        migrations.RemoveField(
            model_name='userclothes',
            name='color',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
