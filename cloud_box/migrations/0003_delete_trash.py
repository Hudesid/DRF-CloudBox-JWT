# Generated by Django 5.1.4 on 2024-12-27 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud_box', '0002_file_is_deleted_alter_file_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Trash',
        ),
    ]
