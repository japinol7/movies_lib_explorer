# Generated by Django 4.1 on 2022-11-16 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_movie_runtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='director',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
