from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Pregunta, Trivia, Admin
from .forms import PreguntaForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def inicio(request):
    return render(request, "usuario/inicio.html")

def nosotros(request):
    return render(request, "usuario/nosotros.html")

@login_required
def crear(request):
    
    context = {
        'trivias': Trivia.objects.all(),
        'preguntas': Pregunta.objects.all(),
    }
    
    return render(request, "usuario/index.html", context)


def crearPregunta(request):
    formulario = PreguntaForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('/')
    return render(request, "usuario/crear.html", {'formulario': formulario})



def editarPregunta(request):
    return render(request, "usuario/editar.html")

def jugar(request):
    trivias = Trivia.objects.all()
    return render(request, "jugar/jugar.html", {'trivias': trivias})

