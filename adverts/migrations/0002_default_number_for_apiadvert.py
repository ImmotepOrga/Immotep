# Generated by Django 4.0.3 on 2022-03-24 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiadvert',
            name='bathrooms',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='apiadvert',
            name='bedrooms',
            field=models.IntegerField(default=0),
        ),
    ]
