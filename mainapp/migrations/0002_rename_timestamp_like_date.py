# Generated by Django 3.2.7 on 2023-05-24 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='timestamp',
            new_name='date',
        ),
    ]