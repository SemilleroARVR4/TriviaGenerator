from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Pregunta, Trivia, Admin
from .forms import PreguntaForm
from django.contrib.auth.decorators import login_required

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


def crearPregunta(request):
    formulario = PreguntaForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('/')
    return render(request, "TGApp/crear.html", {'formulario': formulario})



def editarPregunta(request):
    return render(request, "TGApp/editar.html")

def jugar(request):
    context = {
        'trivias': Trivia.objects.all(),
        'preguntas': Pregunta.objects.all(),
    }
    return render(request, "jugar/jugar.html", context)

