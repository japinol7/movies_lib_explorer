# Generated by Django 4.1 on 2022-11-08 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_movie_title_original'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='runtime',
            field=models.IntegerField(default=0),
        ),
    ]
