# Generated by Django 3.1.4 on 2021-01-05 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0012_auto_20210105_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
