# Generated by Django 3.1 on 2022-06-18 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contribution_management', '0002_contributorguide_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contributorguide',
            old_name='category',
            new_name='skill',
        ),
    ]