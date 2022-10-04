from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Pregunta, Trivia, Admin
from .forms import formPregunta, formTrivia
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def inicio(request):
    return render(request, "TGApp/inicio.html")

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
    preguntas = Pregunta.objects.filter(Trivia=trivias)
    
    initial_data = {

        'Trivia': trivias,
        'pregunta': 'Prueba de que funciona',
        'opcionCorrecta' : 'opcion correcta',
        'opcion2' : 'opcion incorrecta',
        'opcion3' : 'opcion incorrecta',
        'opcion4' : 'opcion incorrecta',
    }
    
    if request.method=='POST':
        formulario = formPregunta(request.POST, initial=initial_data) 
        if formulario.is_valid():
            formulario.save()
            messages.success(request, f'¡Tu pregunta ha sido registrada!')
            return redirect("/crear")
    else:
        formulario = formPregunta(initial=initial_data)
    return render(request, "TGApp/crear.html", {'trivias': trivias, 'preguntas':preguntas, 'formulario': formulario})      


@login_required
def crearNuevaPregunta(request):

    # trivias= Trivia.objects.all()
    # preguntas = Pregunta.objects.filter(Trivia=trivias)
    # initial_data = {

    #     'Trivia': trivias,
    #     'pregunta': 'Prueba de que funciona',
    #     'opcionCorrecta' : 'opcion correcta',
    #     'opcion2' : 'opcion incorrecta',
    #     'opcion3' : 'opcion incorrecta',
    #     'opcion4' : 'opcion incorrecta',
    # }
    if request.method=='POST':
        form = formTrivia(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, f'¡Tu trivia ha sido registrada, ya puedes agregar preguntas!')
            return redirect("/crear")
    else:
        form = formTrivia()

    return render(request, 'TGApp/formTrivia.html', {'form': form})
            


def editarPregunta(request):
    return render(request, "TGApp/editar.html")

def jugar(request):
    context = {
        'trivias': Trivia.objects.all(),
        'preguntas': Pregunta.objects.all(),
    }
    return render(request, "jugar/jugar.html", context)


