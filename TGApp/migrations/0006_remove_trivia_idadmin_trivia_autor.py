# Generated by Django 4.1 on 2022-09-13 01:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TGApp', '0005_pregunta_trivia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trivia',
            name='idAdmin',
        ),
        migrations.AddField(
            model_name='trivia',
            name='autor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
