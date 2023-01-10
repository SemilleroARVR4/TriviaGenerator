from enum import unique
import random
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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
    nombre = models.CharField(max_length=100)
    Tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.Tipo
        
    # def __str__(self):
    #     return '%s %s' % (self.nombre, self.Tipo)

    # def __str__(self):
    #     fila = "Nombre: " + self.nombre + "-" + "Tipo: " + self.Tipo
    #     return fila

    def get_absolute_url(self):
        return reverse('crear')

class Pregunta(models.Model):

    numero_respuestas_permitidas = 1
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trivia = models.ForeignKey(Trivia, on_delete=models.CASCADE, null=True)
    id = models.AutoField(primary_key=True)
    pregunta = models.TextField(verbose_name='Enunciado de la pregunta', null=True)
    opcionCorrecta = models.CharField(max_length=1000, verbose_name='Opcion correcta de la pregunta', null=True)
    opcion2 = models.CharField(max_length=1000, verbose_name='Opcion falsa de la pregunta', null=True)
    opcion3 = models.CharField(max_length=1000, verbose_name='Opcion falsa de la pregunta', null=True)
    opcion4 = models.CharField(max_length=1000, verbose_name='Opcion falsa de la pregunta', null=True)
    respuesta = models.CharField(max_length=1000, verbose_name='respuesta', null=True)
    puntaje = models.DecimalField(verbose_name='Puntaje obtenido', default=0, decimal_places=2, max_digits=10)    

    def __str__(self):
        return self.pregunta

    def get_absolute_url(self):
        return reverse('crear')

    def respuesta_unica(self):
        pass

class PreguntaModelo(models.Model):

    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trivia = models.ForeignKey(Trivia, on_delete=models.CASCADE, null=True)
    id = models.AutoField(primary_key=True)
    pregunta = models.TextField(verbose_name='Enunciado de la pregunta', null=True)
    opcionCorrecta = models.CharField(max_length=1000, verbose_name='Opcion correcta de la pregunta', null=True)
    opcion2 = models.CharField(max_length=1000, verbose_name='Opcion falsa de la pregunta', null=True)
    opcion3 = models.CharField(max_length=1000, verbose_name='Opcion falsa de la pregunta', null=True)
    opcion4 = models.CharField(max_length=1000, verbose_name='Opcion falsa de la pregunta', null=True)
    respuesta = models.CharField(max_length=1000, verbose_name='respuesta', null=True)
    puntaje = models.DecimalField(verbose_name='Puntaje obtenido', default=0, decimal_places=2, max_digits=10)    

    def __str__(self):
        return self.pregunta

class QuizUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    puntaje_total = models.DecimalField(verbose_name='Puntaje total', default=0, decimal_places=2, max_digits=10)


class PreguntasRespondidas(models.Model):
    usuario = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, default=True)
    puntaje_obtenido = models.DecimalField(verbose_name='Puntaje obtenido', default=0, decimal_places=2, max_digits=10)






# Tutorial
class PreguntaQuiz(models.Model):

    NUMERO_DE_RESPUESTAS_PERMITIDAS = 1
    texto = models.TextField(verbose_name='Texto de la pregunta')
    max_puntaje = models.DecimalField(verbose_name='Maximo puntaje', default=3, decimal_places=2, max_digits=10)

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









#COMO LAS OPCIONES DEBEN TENER UN ID PUEDO HACER ESTO   

class PreguntasConOpciones(models.Model):
    pregunta = models.TextField(max_length=100, null=True)
    opcion1 = models.TextField(max_length=100, null=True)
    opcion2 = models.TextField(max_length=100, null=True)
    opcion3 = models.TextField(max_length=100, null=True)
    opcion4 = models.TextField(max_length=100, null=True)
    res = models.CharField(max_length=100, null=True)#entre 1 y 4(# opciones)

    def __str__(self):
        return self.pregunta
# HAY QUE AÑADIR UN CAMPO NO IMPLICITO QUE IDENTFIQUE CUAL ES LA OPCION CORRECTA
# La idea es verificar si la opcion es correcta si el numero coincide con nuestra respuesta



# CORRECT_BONUS CUANTO PUNTAJE DA LA OPCION CORRECTA

    # def starGame():
    #     questionCounter = 0
    #     Score = 0
    #     availableQuestions = PreguntasConOpciones.pregunta.count()

    # def getNewQuestion():
    #     questionCounter = questionCounter + 1
    #     questionIndex = random.randint(0,PreguntasConOpciones.pregunta.count())





# PREGUNTA ACTUAL 
# NECESITAMOS UNA VARIABLE SCORE =0
# POSIBLE PREGUNTA_ACTUAL
# BOOLEANO ACEPTAR_O_NO_RESPUESTAS PARECIDO A RESPUESTA_CORRECTA O NUM_DE_INTENTOS
# CONTADOR DE PREGUNTAS = 0
# PREGUNTAS DISPONIBLES PARECIDO A PREGUNTA ACTUAL 




class Poll(models.Model):
    question = models.TextField()
    option_one = models.CharField(max_length=30)
    option_two = models.CharField(max_length=30)
    option_three = models.CharField(max_length=30)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)

    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count

