# Generated by Django 3.1.5 on 2021-01-24 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0039_auto_20210124_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='floor',
            field=models.IntegerField(max_length=2),
        ),
    ]
