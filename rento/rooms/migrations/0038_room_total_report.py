# Generated by Django 3.1.5 on 2021-01-20 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0037_room_declined_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='total_report',
            field=models.IntegerField(default=0),
        ),
    ]
