# Generated by Django 3.1.5 on 2021-01-18 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0032_auto_20210118_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='day_remaning',
            field=models.IntegerField(default=0),
        ),
    ]
