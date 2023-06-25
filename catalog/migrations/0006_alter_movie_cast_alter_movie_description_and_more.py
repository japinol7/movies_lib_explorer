# Generated by Django 4.2.1 on 2023-06-23 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_actor_alter_director_options_director_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='cast',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.CharField(blank=True, max_length=900),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=90),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title_original',
            field=models.CharField(max_length=90),
        ),
    ]
