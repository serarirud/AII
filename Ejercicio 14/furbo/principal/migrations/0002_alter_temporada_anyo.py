# Generated by Django 3.2.9 on 2021-11-16 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporada',
            name='anyo',
            field=models.CharField(max_length=9),
        ),
    ]