# Generated by Django 4.1 on 2023-01-13 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ElegirRespuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correcta', models.BooleanField(default=False, verbose_name='Es esta la pregunta correcta?')),
                ('texto', models.TextField(verbose_name='Texto de la respuesta')),
            ],
        ),
        migrations.CreateModel(
            name='PreguntaQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(verbose_name='Texto de la pregunta')),
                ('max_puntaje', models.DecimalField(decimal_places=2, default=3, max_digits=10, verbose_name='Maximo puntaje')),
            ],
        ),
        migrations.CreateModel(
            name='Trivia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('Tipo', models.CharField(max_length=100)),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioTrivia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntajeTotal', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Puntaje Total')),
                ('trivia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TGApp.trivia')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizUsuarioTrivia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje_total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Puntaje Total')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PreguntasRespondidasTrivia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correcta', models.BooleanField(default=False, verbose_name='Es esta la respuesta correcta?')),
                ('puntaje_obtenido', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Puntaje Obtenido')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TGApp.preguntaquiz')),
                ('quizUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intentos', to='TGApp.quizusuariotrivia')),
                ('respuesta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TGApp.elegirrespuesta')),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pregunta', models.TextField(null=True, verbose_name='Enunciado de la pregunta')),
                ('opcionCorrecta', models.CharField(max_length=1000, null=True, verbose_name='Opcion correcta de la pregunta')),
                ('opcion2', models.CharField(max_length=1000, null=True, verbose_name='Opcion falsa de la pregunta')),
                ('opcion3', models.CharField(max_length=1000, null=True, verbose_name='Opcion falsa de la pregunta')),
                ('opcion4', models.CharField(max_length=1000, null=True, verbose_name='Opcion falsa de la pregunta')),
                ('respuesta', models.CharField(max_length=1000, null=True, verbose_name='respuesta')),
                ('puntaje', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Puntaje obtenido')),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('trivia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TGApp.trivia')),
            ],
        ),
        migrations.AddField(
            model_name='elegirrespuesta',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opciones', to='TGApp.preguntaquiz'),
        ),
    ]
