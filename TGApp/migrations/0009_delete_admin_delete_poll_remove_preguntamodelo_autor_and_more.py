# Generated by Django 4.1 on 2023-01-12 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TGApp', '0008_poll'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='Poll',
        ),
        migrations.RemoveField(
            model_name='preguntamodelo',
            name='autor',
        ),
        migrations.RemoveField(
            model_name='preguntamodelo',
            name='trivia',
        ),
        migrations.DeleteModel(
            name='PreguntasConOpciones',
        ),
        migrations.DeleteModel(
            name='PreguntaModelo',
        ),
    ]
