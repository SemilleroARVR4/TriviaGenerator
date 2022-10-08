from enum import unique
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# El modelo da las pautas de lo que se va a crear en el admin

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre



class Trivia(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    Tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.Tipo

class Pregunta(models.Model):
    Trivia = models.ForeignKey(Trivia, on_delete=models.CASCADE, null=True)
    id = models.AutoField(primary_key=True)
    pregunta = models.TextField(verbose_name='Enunciado de la pregunta')
    opcionCorrecta = models.CharField(max_length=1000, verbose_name='Opcion correcta de la pregunta')
    opcion2 = models.TextField(verbose_name='Opcion falsa de la pregunta')
    opcion3 = models.TextField(verbose_name='Opcion falsa de la pregunta')
    opcion4 = models.TextField(verbose_name='Opcion falsa de la pregunta',)

    def __str__(self):
        return self.pregunta



