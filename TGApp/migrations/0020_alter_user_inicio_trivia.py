# Generated by Django 4.1 on 2023-03-14 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGApp', '0019_user_inicio_trivia_acceso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_inicio',
            name='trivia',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='trivias'),
        ),
    ]
