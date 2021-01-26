# Generated by Django 3.1.4 on 2021-01-04 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0006_auto_20210104_1633'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='City',
            new_name='Location',
        ),
        migrations.AddField(
            model_name='room',
            name='location',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='room',
            name='city',
            field=models.CharField(max_length=120),
        ),
    ]
