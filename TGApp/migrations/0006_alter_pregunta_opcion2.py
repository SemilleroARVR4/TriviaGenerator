# Generated by Django 4.1 on 2023-02-14 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGApp', '0005_test_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pregunta',
            name='opcion2',
            field=models.CharField(max_length=350, verbose_name='Opcion falsa de la pregunta'),
        ),
    ]
