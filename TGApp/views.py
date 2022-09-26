from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Pregunta, Trivia, Admin
from .forms import PreguntaForm, formTest
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


@login_required
def crearPregunta(request, Trivia_id):

    trivias= Trivia.objects.get(id=Trivia_id)
    preguntas = Pregunta.objects.filter(Trivia=trivias)
    
    return render(request, "TGApp/crear.html", {'trivias': trivias, 'preguntas':preguntas})


@login_required
def crearNuevaPregunta(request):

    formulario = formTest()  
    if request.method=='POST':
        formulario = formTest(data=request.POST) 
        if formulario.is_valid():
            nombre = request.POST.get("nombre")
            
            return redirect("/crear/agregar/nuevo?valido")
            

    return render(request, "TGApp/crearNuevop.html", {'formulario':formulario}) 



def editarPregunta(request):
    return render(request, "TGApp/editar.html")

def jugar(request):
    context = {
        'trivias': Trivia.objects.all(),
        'preguntas': Pregunta.objects.all(),
    }
    return render(request, "jugar/jugar.html", context)


