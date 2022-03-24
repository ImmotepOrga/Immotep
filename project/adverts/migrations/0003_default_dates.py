# Generated by Django 4.0.3 on 2022-03-24 13:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0002_default_number_for_apiadvert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiadvert',
            name='created_date',
            field=models.DateTimeField(default=datetime.date(2022, 3, 24), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='apiadvert',
            name='last_seen',
            field=models.DateTimeField(default=datetime.date(2022, 3, 24), verbose_name='date last seen'),
        ),
        migrations.AlterField(
            model_name='apiadvert',
            name='removed_date',
            field=models.DateTimeField(default=datetime.date(2022, 3, 24), verbose_name='date removed'),
        ),
    ]
