# Generated by Django 4.2.1 on 2023-06-03 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_movie_runtime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=52)),
                ('first_name', models.CharField(blank=True, max_length=52)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
            ],
            options={
                'verbose_name': 'Actor',
                'verbose_name_plural': 'Actors',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.AlterModelOptions(
            name='director',
            options={'ordering': ['last_name', 'first_name'], 'verbose_name': 'Director', 'verbose_name_plural': 'Directors'},
        ),
        migrations.AddField(
            model_name='director',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='movie',
            name='cinematography',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AddField(
            model_name='movie',
            name='decade',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='movie',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='movie',
            name='producer',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AddField(
            model_name='movie',
            name='writer',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.IntegerField(default=0),
        ),
        migrations.AddIndex(
            model_name='director',
            index=models.Index(fields=['last_name', 'first_name'], name='catalog_dir_last_na_a910ee_idx'),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['year', 'title', 'director'], name='catalog_mov_year_4c754a_idx'),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['decade', 'year', 'title', 'director'], name='catalog_mov_decade_78c829_idx'),
        ),
        migrations.AddIndex(
            model_name='actor',
            index=models.Index(fields=['last_name', 'first_name'], name='catalog_act_last_na_43aeab_idx'),
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(blank=True, to='catalog.actor'),
        ),
    ]
