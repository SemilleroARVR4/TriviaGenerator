# Generated by Django 4.1 on 2023-03-03 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGApp', '0015_user_inicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_inicio',
            name='acceso',
            field=models.BooleanField(default=False, verbose_name='Acceso'),
        ),
    ]