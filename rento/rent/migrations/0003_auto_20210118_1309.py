# Generated by Django 3.1.4 on 2021-01-18 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0002_auto_20210118_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='date_paid',
            field=models.DateField(null=True),
        ),
    ]
