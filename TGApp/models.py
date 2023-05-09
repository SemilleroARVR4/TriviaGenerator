from enum import unique
import random
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Trivia(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    Tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.Tipo

    def get_absolute_url(self):
        return reverse('preguntas')

class Pregunta(models.Model):

    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trivia = models.ForeignKey(Trivia, on_delete=models.CASCADE, null=True)
    id = models.AutoField(primary_key=True)
    pregunta = models.TextField(verbose_name='Enunciado de la pregunta', null=True)
    opcionCorrecta = models.CharField(max_length=350, verbose_name='Opcion correcta de la pregunta', null=True)
    opcion2 = models.CharField(max_length=350, verbose_name='Opcion falsa de la pregunta', null=True)
    opcion3 = models.CharField(max_length=350, verbose_name='Opcion falsa de la pregunta', null=True)
    opcion4 = models.CharField(max_length=350, verbose_name='Opcion falsa de la pregunta', null=True)
    puntaje = models.DecimalField(verbose_name='Puntaje obtenido', default=0, decimal_places=2, max_digits=10)   
    archivo = models.FileField(upload_to='archivos', verbose_name="Archivo opcional (imagenes, audios y videos solamente)", blank=True)
    pista =  models.CharField(max_length=350, verbose_name='Pista de la pregunta', blank=True)

    def __str__(self):
        return f"{self.trivia} - {self.pregunta}"

    def get_absolute_url(self):
        return reverse('crear')


    def delete(self, using=None, keep_parents=False):
        if bool(self.archivo):
            self.archivo.storage.delete(self.archivo.name)
        super().delete()
        
class UsuarioTrivia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    puntajeTotal = models.DecimalField(verbose_name='Puntaje Total', default=0, decimal_places=0, max_digits=10)
    trivia = models.ForeignKey(Trivia, on_delete=models.CASCADE, null=False)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.puntajeTotal)

class test_file(models.Model):
    archivo = models.FileField(upload_to='archivos', verbose_name="archivo_a_subir")

    def delete(self, using=None, keep_parents=False):
        self.archivo.storage.delete(self.archivo.name)
        super().delete()

class user_acceso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    acceso = models.BooleanField(verbose_name='Acceso', default=False)

class user_inicio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    acceso = models.BooleanField(verbose_name='Acceso', default=False)
    trivia = models.DecimalField(verbose_name='trivias', default=0, decimal_places=0, max_digits=10)
    trivia_acceso = models.CharField(verbose_name='trivia', max_length=100, blank=True)

    def __str__(self):
        return str(self.usuario)
    
class testChoices(models.Model):
    facil = "fa"
    medio = "me"
    dificil = "di"
    Dificultad = [
        (facil, "facil"),
        (medio, "medio"),
        (dificil, "dificil"),
    ]
    year_in_school = models.CharField(
        max_length=2,
        choices=Dificultad,
        default=facil,
    )

class preguntaChoice(models.Model):
    pregunta = models.CharField(verbose_name='Texto', max_length=100)
    difi = models.ForeignKey(testChoices, on_delete=models.CASCADE)


# Tutorial
class PreguntaQuiz(models.Model):

    NUMERO_DE_RESPUESTAS_PERMITIDAS = 1
    texto = models.TextField(verbose_name='Texto de la pregunta')
    max_puntaje = models.DecimalField(verbose_name='Maximo puntaje', default=3, decimal_places=0, max_digits=10)

    def __str__(self):
        return self.texto
    

class ElegirRespuesta(models.Model):

    MAXIMO_RESPUESTA = 4
    pregunta = models.ForeignKey(PreguntaQuiz, related_name='opciones', on_delete=models.CASCADE)
    correcta = models.BooleanField(verbose_name='Es esta la pregunta correcta?', default=False, null=False)
    texto = models.TextField(verbose_name='Texto de la respuesta')

    def __str__(self):
        return self.texto




class QuizUsuarioTrivia(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    puntaje_total = models.DecimalField(verbose_name='Puntaje Total', default=0, decimal_places=2, max_digits=10)


    def crear_intentos(self, pregunta):
        intento = PreguntasRespondidasTrivia(pregunta=pregunta, quizUser=self)
        intento.save()


    def obtener_nuevas_preguntas(self):
        respondidas = PreguntasRespondidasTrivia.objects.filter(quizUser=self).values_list('pregunta__pk', flat=True)
        preguntas_restantes = PreguntaQuiz.objects.exclude(pk__in=respondidas)
        if not preguntas_restantes.exists():
            return None
        return random.choice(preguntas_restantes)

    def validar_intento(self, pregunta_respondida, respuesta_seleccionada):
        if pregunta_respondida.pregunta_id != respuesta_seleccionada.pregunta_id:
            return 

        pregunta_respondida.respuesta_seleccionada = respuesta_seleccionada
        if respuesta_seleccionada.correcta is True:
            pregunta_respondida.correcta = True
            pregunta_respondida.puntaje_obtenido = respuesta_seleccionada.pregunta.max_puntaje
            pregunta_respondida.respuesta = respuesta_seleccionada

        else:
            pregunta_respondida.respuesta = respuesta_seleccionada

        pregunta_respondida.save()

        self.actualizar_puntaje()

    def actualizar_puntaje(self):
        puntaje_Actualizado = self.intentos.filter(correcta=True).aggregate(models.Sum('puntaje_obtenido'))['puntaje_obtenido__sum']

        self.puntaje_total = puntaje_Actualizado
        self.save()

class PreguntasRespondidasTrivia(models.Model):
    quizUser = models.ForeignKey(QuizUsuarioTrivia, on_delete=models.CASCADE, related_name='intentos')
    pregunta = models.ForeignKey(PreguntaQuiz, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(ElegirRespuesta, on_delete=models.CASCADE, null=True)
    correcta = models.BooleanField(verbose_name='Es esta la respuesta correcta?', default=False, null=False)
    puntaje_obtenido = models.DecimalField(verbose_name='Puntaje Obtenido', default=0, decimal_places=2, max_digits=10)