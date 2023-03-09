from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from .models import Pregunta, Trivia, UsuarioTrivia, test_file, user_acceso, user_inicio
from .forms import formPregunta, test_form
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from random import shuffle
from django.contrib.auth.models import User


def inicio(request):

    if request.user.is_authenticated and not request.user.is_staff:
        usuario = user_inicio.objects.get_or_create(usuario=request.user)
    else:
        usuario = request.user
    
    return render(request, "TGApp/inicio.html", {'usuario':usuario})

def nosotros(request):
    return render(request, "TGApp/nosotros.html")

@login_required
def crear(request):
    
    context = {
        'trivias': Trivia.objects.all(),
        'preguntas': Pregunta.objects.all(),
    }
    
    return render(request, "TGApp/index.html", context)


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
            return redirect("/crear")
    else:
        formulario = formPregunta(initial=initial_data)
    return render(request, "TGApp/crear.html", {'trivias': trivias, 'preguntas':preguntas, 'formulario': formulario}) 


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
    fields = ["trivia", "pregunta", "archivo", "opcionCorrecta", "opcion2", "opcion3", "opcion4",]
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

@login_required
def preguntas(request):
    
    preguntas = Pregunta.objects.filter(autor=request.user).order_by('-trivia')
    contador = preguntas.count()
    print(contador)
    context = {
        'preguntas': preguntas,
        'contar_user':contador
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

        user_groups = request.user.groups.all()
        print(user_groups)

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
            'user_groups': user_groups,
        }
        
        return render(request, 'TGApp/resultados.html', context)

    else:

        trivia = Trivia.objects.get(id=Trivia_id)
        preguntas = Pregunta.objects.filter(trivia=trivia).order_by('?')

        trivias_acceso = Trivia.objects.filter(autor=request.user)
        usuarios = user_inicio.objects.all()

        user_groups = request.user.groups.all()
        print(user_groups)
        contador = preguntas.count()
        # print(preguntas)
        preguntas_options = []


        trivia_lista=""
        for trivia_acceso in trivias_acceso:
            trivias_str = trivia.id
            print(trivias_str)
            triviass = str(trivia.id)
            trivia_lista = trivia_lista + "" + triviass
        print(trivia_lista)

        
        for usuario in usuarios:
            if usuario.usuario == request.user:
                print(usuario.trivia_acceso)
                trivia_lista = usuario.trivia_acceso
        print(trivia_lista)


        for pregunta in preguntas:
            options = [pregunta.opcionCorrecta, pregunta.opcion2, pregunta.opcion3, pregunta.opcion4]#, pregunta.archivo]
            # print(options)
            shuffle(options)
            pregunta_options = {'pregunta': pregunta, 'options': options}
            # print(type(pregunta_options))
            # print(pregunta_options)
            preguntas_options.append(pregunta_options)
        
        context = {
            'preguntas_options': preguntas_options,
            'contar_user':contador,
            'user_groups': user_groups,
            'trivias_acceso': trivias_acceso,
            'usuarios':usuarios,
            'trivia_lista':trivia_lista,
            'trivias_str':trivias_str
            
        }
 
        return render(request, 'jugar/jugarTrivia.html', context)
    





def tablero(request, trivia_id):

    trivia = Trivia.objects.get(id=trivia_id)
    total_usuarios_quiz = UsuarioTrivia.objects.filter(trivia=trivia).order_by('-puntajeTotal')
    contador = total_usuarios_quiz.count()

    context = {
        'trivia':trivia,
        'usuario_quiz':total_usuarios_quiz[:10],
        'contar_user':contador
    }
    return render(request, 'jugar/tablero.html', context)


def puntuaciones(request):

    trivias = Trivia.objects.all()
    context = {
        'trivias':trivias,
    }

    return render(request, 'TGApp/puntuaciones.html', context)



def list(request):
    if request.method == 'POST':
        form = test_form(request.POST, request.FILES)
        if form.is_valid():
            newdoc = test_file(archivo = request.FILES['docfile'])
            newdoc.save()

            return redirect('/test')
    else:
        form = test_form() 

    documents = test_file.objects.all()
    context = {
        'documents': documents, 
        'form': form}
    return render(request, 'TGApp/list.html', context)
    
def show_items(request):
    testes = test_file.objects.all()

    context = {
        'testes': testes,
    }
    
    return render(request, 'TGApp/test.html', context)

def preguntasTest(request):
    
    trivias = Trivia.objects.filter(autor=request.user)

    context = {
        'trivias': trivias,

    }
    return render(request, "TGApp/404.html", context)







def acceso_trivia(request):

    # trivias = Trivia.objects.filter(autor=request.user)
    trivias = Trivia.objects.all()
    
    # usuarios, created = user_acceso.objects.get_or_create(usuario=request.user,)#, acceso=True)
    usuarios = user_inicio.objects.filter(usuario=request.user)

    for usuario in usuarios:
        trivia_lista = usuario.trivia_acceso

    trivia_lista = trivia_lista.split(',')

    trivia_lista = [int(trivia) for trivia in trivia_lista]


    context = {
        'trivias': trivias,
        'usuarios':usuarios,
        'trivia_lista':trivia_lista,
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


# def acceso_trivia_test(request):
#     trivias = Trivia.objects.filter(autor=request.user)
    
#     # Usuario actual
#     usuario_actual = request.user

#     # Usuarios de acceso, todos los usuarios "sin staff"
#     usuarios_acceso =  user_inicio.objects.all()

#     # Verificar si el usuario actual tiene permisos de acceso
#     if not request.user.is_staff :
#         return HttpResponse("No tienes permiso para acceder a esta página")

#     trivia_lista = ""

#     if request.method == 'POST':
#         if usuario_actual == request.user:

#             for trivia in trivias:
#                 # Obtener el usuario al que se le otorgará acceso
#                 usuario_id = request.POST.get('usuario_id')              
                
#                 # Obtener las preguntas seleccionadas                
#                 trivia_seleccionada = request.POST.get(str(trivia.pk))
#                 #FUNCIONAL
#                 print(trivia_seleccionada)
#                 if not trivia_seleccionada:
#                     trivia_seleccionada = 0
#                 else:
#                     # trivia_lista = ','.join(trivia_lista)
#                     trivia_lista = trivia_lista +  trivia_seleccionada + ","


#             user_inicio.objects.update(trivia=trivia_seleccionada)
#             # Obtener el usuario de acceso del usuario seleccionado
#             usuario_acceso_seleccionado = user_inicio.objects.get(usuario_id=usuario_id)
#             usuario_acceso_seleccionado.trivia_acceso = trivia_lista
#             usuario_acceso_seleccionado.save()   

#     context = {
#         'trivias': trivias,
#         'usuarios_acceso': usuarios_acceso,
#         'trivia_lista':trivia_lista
#     }

#     return render(request, "TGApp/acceso_trivia.html", context)





@login_required
def jugarTriviaUsuario(request, Trivia_id):
    
    if request.method == 'POST':
        trivia = Trivia.objects.get(id=Trivia_id)
        QuizUsuario, created = UsuarioTrivia.objects.get_or_create(usuario=request.user, trivia=trivia)

        user_groups = request.user.groups.all()
        print(user_groups)

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
            'user_groups': user_groups,
        }
        
        return render(request, 'TGApp/resultados.html', context)

    else:

        # trivias = Trivia.objects.filter(autor=request.user)
        trivias = Trivia.objects.all()
    
        # usuarios, created = user_acceso.objects.get_or_create(usuario=request.user,)#, acceso=True)
        usuarios = user_inicio.objects.filter(usuario=request.user)

       
        for usuario in usuarios:
            trivia_lista = usuario.trivia_acceso

        trivia_lista = trivia_lista.split(',')

        trivia = Trivia.objects.get(id=Trivia_id)
        preguntas = Pregunta.objects.filter(trivia=trivia).order_by('?')

        trivias_acceso = Trivia.objects.filter(autor=request.user)
        usuarios = user_inicio.objects.all()

        user_groups = request.user.groups.all()
        # print(user_groups)
        contador = preguntas.count()
        # print(preguntas)
        preguntas_options = []

        for pregunta in preguntas:
            options = [pregunta.opcionCorrecta, pregunta.opcion2, pregunta.opcion3, pregunta.opcion4]

            shuffle(options)
            pregunta_options = {'pregunta': pregunta, 'options': options}

            preguntas_options.append(pregunta_options)
        
        context = {
            'trivias':trivias,
            'preguntas_options': preguntas_options,
            'contar_user':contador,
            'user_groups': user_groups,
            'trivias_acceso': trivias_acceso,
            'usuarios':usuarios,
            'trivia_lista':trivia_lista,
            'test':['1','2','10']
            
        }
 
        return render(request, 'TGApp/404.html', context)
    
# @login_required
# def jugarTriviaUsuario(request, Trivia_id):
    
#     if request.method == 'POST':
#         trivia = Trivia.objects.get(id=Trivia_id)
#         QuizUsuario, created = UsuarioTrivia.objects.get_or_create(usuario=request.user, trivia=trivia)

#         user_groups = request.user.groups.all()
#         print(user_groups)

#         preguntas = Pregunta.objects.filter(trivia=trivia).order_by('?')
#         usuarios = UsuarioTrivia.objects.filter(trivia=trivia)        

#         for usuario in usuarios:
#             puntajeUsuario = int(usuario.puntajeTotal)
     
            
#         preguntas_options = []
#         for pregunta in preguntas:
#             options = [pregunta.opcionCorrecta, pregunta.opcion2, pregunta.opcion3, pregunta.opcion4]
#             shuffle(options)
#             pregunta_options = {'pregunta': pregunta, 'options': options}
#             preguntas_options.append(pregunta_options)

        
#         puntaje = 0
#         incorrecta = 0
#         correcta = 0
#         total = 0
#         count = 0
#         puntajeUsuario = 0
#         QuizUsuario.puntajeTotal =0
#         QuizUsuario.save()
        
#         for pregunta_options in preguntas_options:
 
#             opcion_seleccionada = request.POST.get(str(pregunta_options['pregunta'].id))
#             total += 1

#             if opcion_seleccionada == pregunta_options['pregunta'].opcionCorrecta:
#                 puntajeUsuario += 10
#                 puntaje += 10
#                 correcta +=1

#             else:
#                 incorrecta +=1
                
#         percent = puntaje/(total*10) *100 
#         percent = round(percent, 2)

#         QuizUsuario.puntajeTotal += puntajeUsuario
#         QuizUsuario.save()
                   

#         context = {
#             'preguntas':preguntas,
#             'preguntas_options': preguntas_options,
#             'trivia':trivia,
#             'puntaje':puntaje,
#             'incorrecta':incorrecta,
#             'correcta':correcta,
#             'total':total,
#             'count':count,
#             'percent':percent,
#             'puntajeUsuario':puntajeUsuario,
#             'user_groups': user_groups,
#         }
        
#         return render(request, 'TGApp/resultados.html', context)

#     else:

#         trivia = Trivia.objects.get(id=Trivia_id)
#         preguntas = Pregunta.objects.filter(trivia=trivia).order_by('?')

#         trivias_acceso = Trivia.objects.filter(autor=request.user)
#         usuarios = user_inicio.objects.all()

#         user_groups = request.user.groups.all()
#         print(user_groups)
#         contador = preguntas.count()
#         # print(preguntas)
#         preguntas_options = []


#         trivia_lista=""
#         for trivia_acceso in trivias_acceso:
#             trivias_str = trivia.id
#             print(trivias_str)
#             triviass = str(trivia.id)
#             trivia_lista = trivia_lista + "" + triviass
#         print(trivia_lista)

        
#         for usuario in usuarios:
#             if usuario.usuario == request.user:
#                 print(usuario.trivia_acceso)
#                 trivia_lista = usuario.trivia_acceso
#         print(trivia_lista)


#         for pregunta in preguntas:
#             options = [pregunta.opcionCorrecta, pregunta.opcion2, pregunta.opcion3, pregunta.opcion4]#, pregunta.archivo]
#             # print(options)
#             shuffle(options)
#             pregunta_options = {'pregunta': pregunta, 'options': options}
#             # print(type(pregunta_options))
#             # print(pregunta_options)
#             preguntas_options.append(pregunta_options)
        
#         context = {
#             'preguntas_options': preguntas_options,
#             'contar_user':contador,
#             'user_groups': user_groups,
#             'trivias_acceso': trivias_acceso,
#             'usuarios':usuarios,
#             'trivia_lista':trivia_lista,
#             'trivias_str':trivias_str
            
#         }
 
#         return render(request, 'jugar/jugarTriviaUsuario.html', context)