# Generated by Django 3.1.5 on 2021-01-18 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0028_auto_20210118_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='times_featured',
            field=models.IntegerField(default=0),
        ),
    ]
