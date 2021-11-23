# Generated by Django 3.2.9 on 2021-11-23 09:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('genero', models.CharField(max_length=1, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ocupacion',
            fields=[
                ('nombre', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Pelicula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('fecha_estreno', models.DateTimeField()),
                ('imdb_url', models.URLField()),
                ('categorias', models.ManyToManyField(to='principal.Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edad', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('codigo_postal', models.CharField(max_length=10)),
                ('ocupacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.ocupacion')),
                ('sexo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.genero')),
            ],
        ),
        migrations.CreateModel(
            name='Puntuacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pelicula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.pelicula')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.usuario')),
            ],
        ),
    ]