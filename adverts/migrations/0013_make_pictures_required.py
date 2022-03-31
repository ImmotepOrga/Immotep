# Generated by Django 4.0.3 on 2022-03-31 11:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0012_add_greenhouse_gas_advert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='pictures',
            field=models.FileField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='apiadvert',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 31, 11, 19, 29, 224135, tzinfo=utc), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='apiadvert',
            name='last_seen',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 31, 11, 19, 29, 224190, tzinfo=utc), verbose_name='date last seen'),
        ),
    ]