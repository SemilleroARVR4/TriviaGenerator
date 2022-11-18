from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Pregunta, Trivia
from .forms import formPregunta, formTrivia
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


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
    preguntas = Pregunta.objects.filter(trivia=trivias)
    
    initial_data = {
        'trivia': trivias,
        'autor': request.user,
    }   

    if request.method=='POST':
        formulario = formPregunta(request.POST, initial=initial_data) 
        if formulario.is_valid():
            formulario.save()
            messages.success(request, f'¡Tu pregunta ha sido registrada!' )
            return redirect("/preguntas")
    else:
        formulario = formPregunta(initial=initial_data)
    return render(request, "TGApp/crear.html", {'trivias': trivias, 'preguntas':preguntas, 'formulario': formulario}) 

       




# class CrearPregunta(SuccessMessageMixin, CreateView):
#     model = Pregunta
#     template_name = 'TGApp/crear.html'
#     fields = ["pregunta", "opcionCorrecta", "opcion2", "opcion3", "opcion4",]
#     success_message = "¡Tu trivia ha sido creada, ya puedes empezar a agregar preguntas!"

#     def form_valid(self, form):
#         form.instance.autor = self.request.user
#         # trivia = get_object_or_404(Trivia, trivia=self.kwargs['trivia'])
#         # form.instance.trivia = trivia
#         return super(CrearPregunta, self).form_valid(form)








    # def get_object(self):
    #     return super().get_object(queryset)
    # def get_initial(self):
    #     trivia = get_object_or_404(Trivia, Tipo=self.kwargs.get('Tipo'))
    #     return super().get_initial()

    # def get_initial(self):
    #     trivia = get_object_or_404(Trivia, Tipo=self.kwargs.get('Tipo'))
    #     return {
    #         'trivia':trivia,
    #     }
        
        # form.instance.Trivia = Trivia
        # form.instance.pTrivia = self.kwargs.get('pk')
        # Trivia = get_object_or_404(Trivia, slug=self.kwargs['Trivia'])
        
    # def get_initial(self):
    #     Trivia = get_object_or_404(Trivia, Tipo=self.kwargs['Tipo'])
    #     return {
    #         'Trivia':Trivia,
    #     }

    # def get_initial(self):
    #     trivia = get_object_or_404(Trivia, Tipo=self.kwargs.get('Tipo'))
    #     return {
    #         'trivia':Trivia,
    #     }
#     #funcion que usa el usuario para poder modificar cosas solo creadas por el 
#     def test_func(self):
#         Pregunta = self.get_object()
#         if self.request.user == Pregunta.autor:
#             return True
#         return False







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
    fields = ["trivia", "pregunta", "opcionCorrecta", "opcion2", "opcion3", "opcion4",]
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

    # def form_valid(self, form):
    #     form.instance.autor = self.request.user
    #     return super().form_valid(form)

    def test_func(self):
        Pregunta = self.get_object()
        if self.request.user == Pregunta.autor:
            return True
        return False


def correcto(request):
    return render(request, "TGApp/correcto.html")

def preguntas(request):
    context = {
        'trivias': Trivia.objects.all().order_by('-id'),
        'preguntas': Pregunta.objects.all().order_by('-id'),
    }
    return render(request, "TGApp/preguntas.html", context)

 
def jugar(request):
    context = {
        'trivias': Trivia.objects.all(),
        'preguntas': Pregunta.objects.all(),
    }
    return render(request, "jugar/jugar.html", context)

class Quizz(DetailView):
    model = Pregunta

# def jugarQuizz(request, Pregunta_id):

#     context = {
#         'trivias': Trivia.objects.all(),
#         'preguntas': Pregunta.objects.all(),
#         # 'preguntas': Pregunta.objects.get(id=Pregunta_id)
#     }
#     return render(request, "TGApp/jugarQuizz.html", context)

    

