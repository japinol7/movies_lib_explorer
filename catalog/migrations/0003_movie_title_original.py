# Generated by Django 4.1 on 2022-11-06 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_movie_options_movie_cast_movie_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='title_original',
            field=models.CharField(default='or', max_length=60),
            preserve_default=False,
        ),
    ]
