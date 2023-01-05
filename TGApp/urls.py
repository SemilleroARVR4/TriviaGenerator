from django.urls import path
from . import views
from .views import CrearNuevaTrivia, EditarPregunta, EliminarPregunta#, Quizz#, crearPreguntaTest
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    # 'url' 'nombre de la funcion en views' 'titulo'
    path('', views.inicio, name='inicio'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('crear', views.crear, name='crear'),
    path('crear/agregar/<int:Trivia_id>/', views.crearPregunta, name='crearPregunta'),  #aqui dirige el index 
    path('crear/agregar/nuevo', login_required(CrearNuevaTrivia.as_view()), name='crearNuevaTrivia'),
    path('preguntas', views.preguntas, name='preguntas'),
    path('pregunta/<int:pk>/editar/', login_required(EditarPregunta.as_view()), name='EditarPregunta'),
    path('pregunta/<int:pk>/eliminar/', login_required(EliminarPregunta.as_view()), name='EliminarPregunta'),
    path('jugar', views.jugar, name='jugar'), 
    path('jugar/trivia/<int:Trivia_id>', views.jugarTrivia, name='jugarTrivia'),
    path('correcto', views.correcto, name='correcto'),   

    path('jugar/trivia', views.jugarQuiz, name='jugarQuizTrivia'),
    path('resultado/<int:pregunta_respondida_pk>', views.resultado_pregunta, name='resultado'),
    path('tablero', views.tablero, name='tablero'),
   
]