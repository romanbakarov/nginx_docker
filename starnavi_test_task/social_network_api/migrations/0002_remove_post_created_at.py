# Generated by Django 3.1.4 on 2020-12-10 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_network_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='created_at',
        ),
    ]