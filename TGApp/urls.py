from django.urls import path
from . import views
from .views import CrearNuevaTrivia, EditarPregunta, EliminarPregunta
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib.staticfiles.urls import static 

urlpatterns = [
    
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
    path('tablero/<int:trivia_id>', views.tablero, name='tablero'),
    path('puntuaciones', views.puntuaciones, name='puntuaciones'),

    path('test', views.list, name='test'),
    path('test2', views.show_items, name='test2'),
    path('preguntass', views.preguntasTest, name='preguntasTest'),

    path('jugarUser', views.acceso_trivia, name='acceso'),

    path('jugarUserr', views.acceso_trivia_test, name='acceso_test'),


    path('jugar/trivia/<int:Trivia_id>/user', views.jugarTriviaUsuario, name='jugarTriviaUsuario'),

 
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)