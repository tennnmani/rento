# Generated by Django 3.1.5 on 2021-01-19 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0036_room_day_remaning'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='declined_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
