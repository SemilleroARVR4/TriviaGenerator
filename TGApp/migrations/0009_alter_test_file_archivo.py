# Generated by Django 4.1 on 2023-02-14 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGApp', '0008_alter_pregunta_opcion2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test_file',
            name='archivo',
            field=models.FileField(upload_to=None, verbose_name='archivo'),
        ),
    ]
