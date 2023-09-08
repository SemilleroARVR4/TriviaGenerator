import sys
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from .models import Pregunta, Trivia, UsuarioTrivia, test_file, user_acceso, user_inicio, CodeSnippet
from .forms import formPregunta, test_form
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from random import shuffle
import subprocess



def inicio(request):

    if request.user.is_authenticated and not request.user.is_staff:
        usuario = user_inicio.objects.get_or_create(usuario=request.user)
    else:
        usuario = request.user
    
    return render(request, "TGApp/inicio.html", {'usuario':usuario})

def nosotros(request):
    return render(request, "TGApp/nosotros.html")
    

class CrearNuevaTrivia(SuccessMessageMixin, CreateView):
    model = Trivia
    template_name = 'TGApp/formTrivia.html'
    fields = ['nombre', 'Tipo']
    success_message = "¡Tu trivia ha sido registrada, ya puedes agregar preguntas!"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(CrearNuevaTrivia, self).get_form(form_class)
        form.fields['nombre'].widget.attrs ={'placeholder': 'Nombre de la trivia'}
        form.fields['Tipo'].widget.attrs ={'placeholder': 'Tipo de trivia'}
        return form
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class EditarPregunta(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Pregunta
    template_name = 'TGApp/editarPregunta.html'
    fields = ["pregunta", "archivo", "opcionCorrecta", "opcion2", "opcion3", "opcion4",]
    success_message = "¡Tu pregunta ha sido actualizada correctamente!"
    success_url = reverse_lazy('preguntas')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    #funcion que usa el usuario para poder modificar cosas solo creadas por el 
    def test_func(self):
        Pregunta = self.get_object()
        if self.request.user == Pregunta.autor:
            return True
        return False



        

class EliminarPregunta(SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Pregunta
    template_name = 'TGApp/eliminarPregunta.html'
    success_url = reverse_lazy('preguntas')
    success_message = "¡Tu pregunta ha sido eliminada correctamente!"

    def test_func(self):
        Pregunta = self.get_object()
        if self.request.user == Pregunta.autor:
            return True
        return False
    
class EditarTrivia(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Trivia
    template_name = 'TGApp/editarTrivia.html'
    fields = ["nombre", "Tipo"]
    success_message = "¡Tu trivia ha sido actualizada correctamente!"
    success_url = reverse_lazy('preguntas')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        Trivia = self.get_object()
        if self.request.user == Trivia.autor:
            return True
        return False
    
class EliminarTrivia(SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Trivia
    template_name = 'TGApp/eliminarTrivia.html'
    success_url = reverse_lazy('preguntas')
    success_message = "¡Tu trivia ha sido eliminada correctamente!"

    def test_func(self):
        Trivia = self.get_object()
        if self.request.user == Trivia.autor:
            return True
        return False

@login_required
def preguntas(request):
   
    preguntas = Pregunta.objects.filter(autor=request.user).order_by('-trivia')
    contador = preguntas.count()
    print(contador)

    trivias = Trivia.objects.all()
    contador_trivias = trivias.count()

    trivia_lista = []
    pregunta_lista = []
    for trivia in trivias:
        trivia_lista.append(trivia.id)

    for pregunta in preguntas:
        pregunta_lista.append(pregunta.trivia.id)
    
    context = {
        'preguntas': preguntas,
        'trivias': trivias,
        'contar_user':contador,
        'contador_trivias':contador_trivias,
        'trivia_lista':trivia_lista,
        'pregunta_lista':pregunta_lista
        
    }
    return render(request, "TGApp/preguntas.html", context)


@login_required
def jugar(request):
    trivias = Trivia.objects.all()

    context = {
        'trivias':trivias,
    }
    return render(request, 'jugar/jugar.html', context)


        

@login_required
def jugarTrivia(request, Trivia_id):
    
    if request.method == 'POST':
        trivia = Trivia.objects.get(id=Trivia_id)
        QuizUsuario, created = UsuarioTrivia.objects.get_or_create(usuario=request.user, trivia=trivia)

        preguntas = Pregunta.objects.filter(trivia=trivia).order_by('?')
        usuarios = UsuarioTrivia.objects.filter(trivia=trivia)        

        for usuario in usuarios:
            puntajeUsuario = int(usuario.puntajeTotal)
     
            
        preguntas_options = []
        for pregunta in preguntas:
            options = [pregunta.opcionCorrecta, pregunta.opcion2, pregunta.opcion3, pregunta.opcion4]
            shuffle(options)
            pregunta_options = {'pregunta': pregunta, 'options': options}
            preguntas_options.append(pregunta_options)

        
        puntaje = 0
        incorrecta = 0
        correcta = 0
        total = 0
        count = 0
        puntajeUsuario = 0
        QuizUsuario.puntajeTotal =0
        QuizUsuario.save()
        
        for pregunta_options in preguntas_options:
 
            opcion_seleccionada = request.POST.get(str(pregunta_options['pregunta'].id))
            total += 1

            if opcion_seleccionada == pregunta_options['pregunta'].opcionCorrecta:
                puntajeUsuario += 10
                puntaje += 10
                correcta +=1

            else:
                incorrecta +=1
                
        percent = puntaje/(total*10) *100 
        percent = round(percent, 2)

        QuizUsuario.puntajeTotal += puntajeUsuario
        QuizUsuario.save()
                   

        context = {
            'preguntas':preguntas,
            'preguntas_options': preguntas_options,
            'trivia':trivia,
            'puntaje':puntaje,
            'incorrecta':incorrecta,
            'correcta':correcta,
            'total':total,
            'count':count,
            'percent':percent,
            'puntajeUsuario':puntajeUsuario,
        }
        
        return render(request, 'TGApp/resultados.html', context)

    else:

        trivia = Trivia.objects.get(id=Trivia_id)
        preguntas = Pregunta.objects.filter(trivia=trivia).order_by('?')

        trivias_acceso = Trivia.objects.filter(autor=request.user)
        usuarios = user_inicio.objects.all()


        contador = preguntas.count()
        preguntas_options = []

        for pregunta in preguntas:
            options = [pregunta.opcionCorrecta, pregunta.opcion2, pregunta.opcion3, pregunta.opcion4]
            shuffle(options)
            pregunta_options = {'pregunta': pregunta, 'options': options}
            preguntas_options.append(pregunta_options)
        
        context = {
            'preguntas_options': preguntas_options,
            'contar_user':contador,
            'trivias_acceso': trivias_acceso,
            'usuarios':usuarios,            
        }
 
        return render(request, 'jugar/jugarTrivia.html', context)
    




def tablero(request, trivia_id):

    trivia = Trivia.objects.get(id=trivia_id)
    total_usuarios_quiz = UsuarioTrivia.objects.filter(trivia=trivia).order_by('-puntajeTotal', '-fecha')
    contador = total_usuarios_quiz.count()

    context = {
        'trivia':trivia,
        'usuario_quiz':total_usuarios_quiz[:5],
        'contar_user':contador
    }
    return render(request, 'jugar/tablero.html', context)

def tableroUsers(request, trivia_id):

    trivia = Trivia.objects.get(id=trivia_id)
    total_usuarios_quiz = UsuarioTrivia.objects.filter(trivia=trivia).order_by('-puntajeTotal', '-fecha')
    contador = total_usuarios_quiz.count()

    context = {
        'trivia':trivia,
        'usuario_quiz':total_usuarios_quiz,
        'contar_user':contador
    }
    return render(request, 'jugar/tableroUsuarios.html', context)


def puntuaciones(request):

    trivias = Trivia.objects.all()
    context = {
        'trivias':trivias,
    }

    return render(request, 'TGApp/puntuaciones.html', context)

    




def list(request, Trivia_id):

    trivias = Trivia.objects.get(id=Trivia_id)
    preguntas = Pregunta.objects.filter(trivia=trivias).order_by('?')
    trivias = str(trivias.id)
    usuarios = user_inicio.objects.filter(usuario=request.user)
    for usuario in usuarios:
        trivia_lista = usuario.trivia_acceso
        
    trivia_lista = trivia_lista.split(",")
    contador = preguntas.count()
    preguntas_options = []

    contador_preguntas = 0
    aceptar_respuestas = False
    for pregunta in preguntas:
            options = [pregunta.opcionCorrecta, pregunta.opcion2, pregunta.opcion3, pregunta.opcion4]
            shuffle(options)
            pregunta_options = {'pregunta': pregunta, 'options':options}
            preguntas_options.append(pregunta_options)

    print(pregunta_options)
    # contador_preguntas = preguntas_options.count()
    print(len(preguntas_options))
    print(type(preguntas_options))
# preguntas_options<---------- Estas son mis preguntas disponibles 

    contador_preguntas += 1
    if contador_preguntas >= len(preguntas_options):
        aceptar_respuestas = True
    
    print(preguntas_options[1])

    context = {
            'contador_preguntas':contador_preguntas,
            'pregunta_options': pregunta_options,
            'trivias':trivias,
            'preguntas_options': preguntas_options,
            'contar_user':contador,
            'usuarios':usuarios,
            'trivia_lista':trivia_lista,     
        }

    return render(request, 'TGApp/list.html', context)
    
def show_items(request):
    
    trivias = Trivia.objects.filter(autor=request.user)
    
    # Usuario actual
    usuario_actual = request.user

    # Usuarios de acceso, todos los usuarios "sin staff"
    usuarios_acceso = user_inicio.objects.all()


    trivia_seleccionadas = []
    #Primero obtener el usuario, despues poner asignar la trivia
    if request.method == 'POST':
        if usuario_actual == request.user:

            for trivia in trivias:
                # Obtener el usuario al que se le otorgará acceso
                usuario_id = request.POST.get('usuario') 
                print("ESte es el id del usuario")
                print(usuario_id)             
                
                # Obtener las preguntas seleccionadas                
                trivia_seleccionada = request.POST.get(str(trivia.pk))
                #FUNCIONAL
                print(trivia_seleccionada)
                if not trivia_seleccionada:
                    trivia_seleccionada = 0
                else:
                    trivia_seleccionadas.append(trivia_seleccionada)
            print(trivia_seleccionadas)
            # Convertir la lista de selecciones de trivia en una cadena separada por comas
            trivia_lista = ','.join(trivia_seleccionadas)
            print(trivia_lista)

            # Actualizar el modelo user_inicio con las selecciones de trivia
            user_inicio.objects.filter(id=usuario_id).update(trivia_acceso=trivia_lista)
        messages.success(request, f'¡Las preguntas han sido asignadas al usuario ' + str(user_inicio.objects.get(usuario=usuario_id)) +'!' )   

    context = {
        'trivias': trivias,
        'usuarios_acceso': usuarios_acceso,
    }


    return render(request, 'TGApp/404.html', context)


def acceso_trivia(request):

    trivias = Trivia.objects.all()
    usuarios = user_inicio.objects.filter(usuario=request.user)
    
    for usuario in usuarios:
        if usuario.trivia_acceso == "":
            trivia_lista = '0'
        else:
            trivia_lista = usuario.trivia_acceso
    
    trivia_lista = trivia_lista.split(",")
    valores = trivia_lista

    if valores[0] == '0':
        valores = 0
    else:   
        valores = [int(valor) for valor in valores]

    
    context = {
        'trivias': trivias,
        'valores':valores,
    }
    
    return render(request, "TGApp/inicioJugar.html", context)



def acceso_trivia_test(request):
    trivias = Trivia.objects.filter(autor=request.user)
    
    # Usuario actual
    usuario_actual = request.user

    # Usuarios de acceso, todos los usuarios "sin staff"
    usuarios_acceso = user_inicio.objects.all()

    # Verificar si el usuario actual tiene permisos de acceso
    if not request.user.is_staff :
        return HttpResponse("No tienes permiso para acceder a esta página")
    
    trivia_seleccionadas = []
    #Primero obtener el usuario, despues poner asignar la trivia
    if request.method == 'POST':
        if usuario_actual == request.user:

            for trivia in trivias:
                # Obtener el usuario al que se le otorgará acceso
                usuario_id = request.POST.get('usuario_id') 
                print("ESte es el id del usuario")
                print(usuario_id)             
                
                # Obtener las preguntas seleccionadas                
                trivia_seleccionada = request.POST.get(str(trivia.pk))
                #FUNCIONAL
                print(trivia_seleccionada)
                if not trivia_seleccionada:
                    trivia_seleccionada = 0
                else:
                    trivia_seleccionadas.append(trivia_seleccionada)
            print(trivia_seleccionadas)
            # Convertir la lista de selecciones de trivia en una cadena separada por comas
            trivia_lista = ','.join(trivia_seleccionadas)
            print(trivia_lista)

            # Actualizar el modelo user_inicio con las selecciones de trivia
            user_inicio.objects.filter(usuario_id=usuario_id).update(trivia_acceso=trivia_lista)
        messages.success(request, f'¡Las preguntas han sido asignadas al usuario ' + str(user_inicio.objects.get(usuario=usuario_id)) +'!' )   

    context = {
        'trivias': trivias,
        'usuarios_acceso': usuarios_acceso,
    }

    return render(request, "TGApp/acceso_trivia.html", context)



@login_required
def jugarTriviaUsuario(request, Trivia_id):
    
    if request.method == 'POST':
        trivia = Trivia.objects.get(id=Trivia_id)
        QuizUsuario = UsuarioTrivia.objects.create(usuario=request.user, trivia=trivia)


        preguntas = Pregunta.objects.filter(trivia=trivia).order_by('?')
        usuarios = UsuarioTrivia.objects.filter(trivia=trivia)       
        

        for usuario in usuarios:
            puntajeUsuario = int(usuario.puntajeTotal)
     
            
        preguntas_options = []
        for pregunta in preguntas:
            options = [pregunta.opcionCorrecta, pregunta.opcion2, pregunta.opcion3, pregunta.opcion4]
            shuffle(options)
            pregunta_options = {'pregunta': pregunta, 'options': options}
            preguntas_options.append(pregunta_options)

            
            # pruebarequest = request.POST.get("nombre")
            # print(pruebarequest) 
        
        puntaje = 0
        incorrecta = 0
        correcta = 0
        total = 0
        count = 0
        puntajeUsuario = 0
        QuizUsuario.puntajeTotal =0
        QuizUsuario.save()
        
        for pregunta_options in preguntas_options:
 
            opcion_seleccionada = request.POST.get(str(pregunta_options['pregunta'].id))
            total += 1

            if opcion_seleccionada == pregunta_options['pregunta'].opcionCorrecta:
                puntajeUsuario += 10
                puntaje += 10
                correcta +=1

            else:
                incorrecta +=1
                
        percent = puntaje/(total*10) *100 
        percent = round(percent, 2)

        QuizUsuario.puntajeTotal += puntajeUsuario
        QuizUsuario.save()

        tiempo_transcurrido = request.POST.get('timer')
        print(tiempo_transcurrido)
        js = request.POST.get('js')   
        print(js)  
        if js == None:
            js = 2              

        context = {
            'preguntas_options': preguntas_options,
            'trivia':trivia,
            'puntaje':puntaje,
            'incorrecta':incorrecta,
            'correcta':correcta,
            'total':total,
            'count':count,
            'percent':percent,
            'puntajeUsuario':puntajeUsuario,
            'time': request.POST.get('timer'),
            'tiempo_transcurrido': tiempo_transcurrido,
            'js':js

        }
        
        return render(request, 'TGApp/resultados.html', context)

    else:

        trivias = Trivia.objects.get(id=Trivia_id)
        preguntas = Pregunta.objects.filter(trivia=trivias).order_by('?')
        trivias = str(trivias.id)
        usuarios = user_inicio.objects.filter(usuario=request.user)
        for usuario in usuarios:
            trivia_lista = usuario.trivia_acceso
        
        trivia_lista = trivia_lista.split(",")
        contador = preguntas.count()
        preguntas_options = []

        for pregunta in preguntas:
            options = [pregunta.opcionCorrecta, pregunta.opcion2, pregunta.opcion3, pregunta.opcion4]
            print(options)
            print("Esta imprimiendo esto")
            shuffle(options)
            pregunta_options = {'pregunta': pregunta, 'options': options}
            preguntas_options.append(pregunta_options)

        context = {
            'trivias':trivias,
            'preguntas_options': preguntas_options,
            'contar_user':contador,
            'usuarios':usuarios,
            'trivia_lista':trivia_lista,     
        }

        return render(request, 'jugar/jugarTriviaUsuario.html', context)
    
def configuraciones(request):

    preguntas = Pregunta.objects.all()
    trivias = Trivia.objects.all()
    contador = preguntas.count()

    pregunta_lista = []
    # for trivia in trivias:
    #     pregunta_lista.append(trivia.nombre)

    for trivia in trivias:
        pregunta_lista.append(trivia.nombre)
        
    for pregunta in preguntas:
        
        pregunta_lista.append(pregunta.pregunta)
        pregunta_lista.append(pregunta.opcionCorrecta)
        pregunta_lista.append(pregunta.opcion2)
    context  = {
        'preguntas':preguntas,
        'trivias':trivias,
        'contador':contador,
        'pregunta_lista':pregunta_lista
    }

    return render(request, 'TGApp/configuraciones.html', context)



def funcion(request, Trivia_id):

    if request.method == 'POST':
        trivia = Trivia.objects.get(id=Trivia_id)
        QuizUsuario = UsuarioTrivia.objects.create(usuario=request.user, trivia=trivia)


        preguntas = Pregunta.objects.filter(trivia=trivia).order_by('?')
        usuarios = UsuarioTrivia.objects.filter(trivia=trivia)       
        

        for usuario in usuarios:
            puntajeUsuario = int(usuario.puntajeTotal)
     
            
        preguntas_options = []
        for pregunta in preguntas:
            options = [pregunta.opcionCorrecta, pregunta.opcion2, pregunta.opcion3, pregunta.opcion4]
            shuffle(options)
            pregunta_options = {'pregunta': pregunta, 'options': options}
            preguntas_options.append(pregunta_options)
        
        puntaje = 0
        incorrecta = 0
        correcta = 0
        total = 0
        count = 0
        puntajeUsuario = 0
        QuizUsuario.puntajeTotal =0
        QuizUsuario.save()
        
        for pregunta_options in preguntas_options:
 
            opcion_seleccionada = request.POST.get(str(pregunta_options['pregunta'].id))
            total += 1

            if opcion_seleccionada == pregunta_options['pregunta'].opcionCorrecta:
                puntajeUsuario += 10
                puntaje += 10
                correcta +=1

            else:
                incorrecta +=1
                
        percent = puntaje/(total*10) *100 
        percent = round(percent, 2)

        QuizUsuario.puntajeTotal += puntajeUsuario
        QuizUsuario.save()         

        context = {
            'preguntas_options': preguntas_options,
            'trivia':trivia,
            'puntaje':puntaje,
            'incorrecta':incorrecta,
            'correcta':correcta,
            'total':total,
            'count':count,
            'percent':percent,
            'puntajeUsuario':puntajeUsuario,
        }
        
        return render(request, 'TGApp/resultados.html', context)

    else:

        trivias = Trivia.objects.get(id=Trivia_id)
        preguntas = Pregunta.objects.filter(trivia=trivias).order_by('?')
        trivias = str(trivias.id)
        usuarios = user_inicio.objects.filter(usuario=request.user)
        for usuario in usuarios:
            trivia_lista = usuario.trivia_acceso
        
        trivia_lista = trivia_lista.split(",")
        contador = preguntas.count()
        preguntas_options = []

        for pregunta in preguntas:
            options = [pregunta.opcionCorrecta, pregunta.opcion2, pregunta.opcion3, pregunta.opcion4]
            print(options)
            print("Esta imprimiendo esto")
            shuffle(options)
            pregunta_options = {'pregunta': pregunta, 'options': options}
            preguntas_options.append(pregunta_options)
        print(type(pregunta_options))
        context = {
            'pregunta_options':pregunta_options,
            'trivias':trivias,
            'preguntas_options': preguntas_options,
            'contar_user':contador,
            'usuarios':usuarios,
            'trivia_lista':trivia_lista,     
        }

        return render(request, 'TGApp/test23.html', context)
    

def pregunta(request, Trivia_id, pregunta_num):
    trivia = Trivia.objects.get(id=Trivia_id)
    preguntas = Pregunta.objects.filter(trivia=trivia).order_by('?')
    usuarios = UsuarioTrivia.objects.filter(trivia=trivia)
    pregunta_options = None

    for usuario in usuarios:
        puntajeUsuario = int(usuario.puntajeTotal)
    
    if request.method == 'POST':
        preguntas_options = request.session.get('preguntas_options')
        pregunta_options = preguntas_options[pregunta_num-1]
        opcion_seleccionada = request.POST.get(str(pregunta_options['pregunta'].id))
        total = 1

        if opcion_seleccionada == pregunta_options['pregunta'].opcionCorrecta:
            puntajeUsuario = puntajeUsuario + 10

        QuizUsuario = UsuarioTrivia.objects.create(usuario=request.user, trivia=trivia, puntajeTotal=puntajeUsuario)
        QuizUsuario.save()

        if pregunta_num < preguntas.count():
            return redirect('pregunta', Trivia_id=Trivia_id, pregunta_num=pregunta_num+1)
        else:
            return redirect('resultados', Trivia_id=Trivia_id)

    else:
        preguntas_options = []
        for pregunta in preguntas:
            options = [pregunta.opcionCorrecta, pregunta.opcion2, pregunta.opcion3, pregunta.opcion4]
            shuffle(options)
            pregunta_options = {'pregunta': pregunta, 'options': options}
            preguntas_options.append(pregunta_options)
        
        request.session['preguntas_options'] = preguntas_options
        pregunta_options = preguntas_options[pregunta_num-1]

    context = {
        'pregunta_options': pregunta_options,
        'trivia':trivia,
        'pregunta_num': pregunta_num,
    }
    
    return render(request, 'TGApp/pregunta.html', context)









posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 3',
        'content': 'Third post content',
        'date_posted': 'August 31, 2018'
    }
]

quests = [
    {
        "category":"Animals",
        "type":"multiple",
        "difficulty":"easy",
        "question":"How many legs do butterflies have?",
        "correct_answer":"6",
        "incorrect_answers":["2","4","0"]
    }

]

preguntaMs = [
    {
        "autor":"Stiven",
        "trivia":"Matematica",
        "pregunta": "cuanto es 2+2",
        "respuesta":"4",
        "opcion_1":'3',
        "opcion_2":'5',
        "opcion_3":'1',
    }
]


def asdfghj(request):
    context = {
        'posts': posts,
        'quests': quests,
        'preguntaMs':preguntaMs
    }
    return render(request, 'TGApp/asdf.html', context)

def nuevo_test(request):
    preguntas = Pregunta.objects.order_by('?')
    preguntas_options = []
    for pregunta in preguntas:
            options = [pregunta.opcionCorrecta, pregunta.opcion2, pregunta.opcion3, pregunta.opcion4]
            shuffle(options)
            pregunta_options = {'pregunta': pregunta, 'options': options}
            preguntas_options.append(pregunta_options)
    context = {
        'preguntas': Pregunta.objects.order_by('?'),
        'pregunta_options': pregunta_options,
    }
    return render(request, 'TGApp/nuevo.html', context)



def resultado(request):
    if request.method == 'POST':
        mensaje = int(request.POST.get("trivia"))
        print(mensaje)
    return render(request, 'TGApp/crear.html', {'mensaje':mensaje})


def runcode(request):    
    trivias = Trivia.objects.all()
    if request.method == 'POST':
        for trivia in trivias:             
                trivia_seleccionada = request.POST.get(trivia)
        codeareadata = request.POST.get("codearea")
        trivia_id = request.POST.get(trivia)
    
        try:
            original_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')
            exec(codeareadata)
            sys.stdout.close()

            sys.stdout = original_stdout

            output = open('file.txt', 'r').read()
        
        except Exception as e:
            
            sys.stdout = original_stdout
            output = e
    #     context = {
    #     'codeareadata' : codeareadata,
    #     'code' : codeareadata,
    #     'output': output
    # }
    #     return redirect("crearPregunta", 1)
    
    context = {
        'codeareadata' : codeareadata,
        'code' : codeareadata,
        'output': output,
        
    }
    return render(request, "TGApp/crear.html", context)
    
@login_required
def crearPregunta(request, Trivia_id):

    trivias= Trivia.objects.get(id=Trivia_id)
    preguntas = Pregunta.objects.filter(trivia=trivias)
    
    initial_data = {
        'trivia': trivias,
        'autor': request.user,
    }   

    if request.method=='POST':
        formulario = formPregunta(request.POST, request.FILES, initial=initial_data) 

        if formulario.is_valid():
            formulario.save()
            messages.success(request, f'¡Tu pregunta ha sido registrada!' )
            return redirect("/preguntas")
    else:
        formulario = formPregunta(initial=initial_data)

    context = {
        'trivias': trivias, 
        'preguntas':preguntas, 
        'formulario': formulario
        }
    return render(request, "TGApp/crear.html", context) 








def start_game(request):
    return render(request, "TGApp/game.html")

def compiler(request):
    trivias = Trivia.objects.all()
    if request.method == 'POST':
        Trivia_id = int(request.POST.get("trivia"))
        codeareadata = request.POST.get("codearea")

        
        try:
            original_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')
            exec(codeareadata)
            sys.stdout.close()

            sys.stdout = original_stdout

            output = open('file.txt', 'r').read()
        
        except Exception as e:
            
            sys.stdout = original_stdout
            output = e

    
    # context = {
    #     'codeareadata' : codeareadata,
    #     'code' : codeareadata,
    #     'output': output,
        messages.success(request, f'' + output )   
        # return HttpResponseRedirect(reverse('crearPregunta', Trivia_id=Trivia_id, kwargs={'num':num}))
        return redirect('crearPregunta', Trivia_id=Trivia_id)
        # context = {
            # 'trivias':Trivia_id
        # }
        # return redirect('start_game') #name url
        
    return render(request, 'TGApp/OldCompiler.html', {'trivias' : trivias})



def compile_view(request):

    trivias = Trivia.objects.all()
    if request.method == 'POST':
        Trivia_id = request.POST.get("trivia")
        if Trivia_id == None:
            messages.success(request, f'Debes seleccionar una trivia')
            return render(request, 'TGApp/compilador.html', {"trivias":trivias})
        source_code = request.POST.get('source_code')
        
        output = execute_code(source_code)
        # code_snippet = CodeSnippet.objects.create(codigo=source_code, salida=output)
        messages.success(request, f'' + output )
        return redirect('crearPregunta', Trivia_id=Trivia_id)
    
        
        
    else:
        return render(request, 'TGApp/compilador.html', {"trivias":trivias})
    

def execute_code(source_code):
    try:
        result = subprocess.run(['python', '-c', source_code], capture_output=True, text=True, timeout=5)
        output = result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        output = e.output
    except subprocess.TimeoutExpired:
        output = 'El tiempo de ejecución excedió el límite.'
    return output

