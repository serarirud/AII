# Generated by Django 3.2.9 on 2021-11-16 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0002_alter_temporada_anyo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jornada',
            name='fecha',
            field=models.CharField(max_length=50),
        ),
    ]
