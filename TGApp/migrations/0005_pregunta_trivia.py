# Generated by Django 4.1 on 2022-09-10 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TGApp', '0004_alter_trivia_idadmin'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregunta',
            name='Trivia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='TipoTrivia', to='TGApp.trivia'),
        ),
    ]
