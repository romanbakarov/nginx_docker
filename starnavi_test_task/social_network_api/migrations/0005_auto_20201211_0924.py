# Generated by Django 3.1.4 on 2020-12-11 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network_api', '0004_auto_20201211_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='like',
            field=models.BooleanField(default=True),
        ),
    ]
