from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Pregunta, Trivia, Admin
from .forms import PreguntaForm, formTest, formularioTest
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
    
    initial_data = {

        'Trivia': trivias,
        'pregunta': 'Prueba de que funciona',
        'opcionCorrecta' : 'opcion correcta',
        'opcion2' : 'opcion incorrecta',
        'opcion3' : 'opcion incorrecta',
        'opcion4' : 'opcion incorrecta',
    }
    
    if request.method=='POST':
        formulario = formularioTest(request.POST, initial=initial_data) 
        # form.fields["Email"].initial = GetEmailString()
        if formulario.is_valid():
            formulario.save()
            return redirect("/crear")
    else:
        formulario = formularioTest(initial=initial_data)
    return render(request, "TGApp/crear.html", {'trivias': trivias, 'preguntas':preguntas, 'formulario': formulario})      
    # return redirect("nosotros")
    # return redirect("TGApp/crear.html", {'trivias': trivias, 'preguntas':preguntas, 'formulario': formulario})

# return render(request, "TGApp/crear.html", {'trivias': trivias, 'preguntas':preguntas, 'formulario': formulario})


# ABRE LA VISTA CON EL ID
# @login_required
# def crearPregunta(request, Trivia_id):

#     trivias= Trivia.objects.get(id=Trivia_id)
#     preguntas = Pregunta.objects.filter(Trivia=trivias)
    
    

#     return render(request, "TGApp/crear.html", {'trivias': trivias, 'preguntas':preguntas})
# ABRE LA VISTA CON EL ID




@login_required
def crearNuevaPregunta(request):

    if request.method=='POST':
        form = formularioTest(request.POST) 
        if form.is_valid():
            form.save()
    else:
        form = formularioTest()

    return render(request, 'TGApp/form.html', {'form': form})
            



def editarPregunta(request):
    return render(request, "TGApp/editar.html")

def jugar(request):
    context = {
        'trivias': Trivia.objects.all(),
        'preguntas': Pregunta.objects.all(),
    }
    return render(request, "jugar/jugar.html", context)


