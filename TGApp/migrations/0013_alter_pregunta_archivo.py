# Generated by Django 4.1 on 2023-02-14 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGApp', '0012_pregunta_archivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pregunta',
            name='archivo',
            field=models.FileField(blank=True, upload_to='archivos', verbose_name='archivo_a_subir'),
        ),
    ]
