from django.urls import path
from . import views
from .views import CrearNuevaTrivia, EditarPregunta, EliminarPregunta, EditarTrivia, EliminarTrivia
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib.staticfiles.urls import static 

urlpatterns = [
    
    path('', views.inicio, name='inicio'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('crear/agregar/<int:Trivia_id>/', views.crearPregunta, name='crearPregunta'),  #aqui dirige el index 
    path('crear/agregar/nuevo', login_required(CrearNuevaTrivia.as_view()), name='crearNuevaTrivia'),
    path('preguntas', views.preguntas, name='preguntas'),
    path('pregunta/<int:pk>/editar/', login_required(EditarPregunta.as_view()), name='EditarPregunta'),
    path('pregunta/<int:pk>/eliminar/', login_required(EliminarPregunta.as_view()), name='EliminarPregunta'),

    path('trivia/<int:pk>/editar/', login_required(EditarTrivia.as_view()), name='EditarTrivia'),
    path('trivia/<int:pk>/eliminar/', login_required(EliminarTrivia.as_view()), name='EliminarTrivia'),

    path('jugar', views.jugar, name='jugar'), 
    path('jugar/trivia/<int:Trivia_id>', views.jugarTrivia, name='jugarTrivia'),
    path('tablero/<int:trivia_id>', views.tablero, name='tablero'),
    path('tableroUsers/<int:trivia_id>', views.tableroUsers, name='tableroUsers'),
    path('puntuaciones', views.puntuaciones, name='puntuaciones'),

    path('test/<int:Trivia_id>', views.list, name='test'),
    path('test2', views.show_items, name='test2'),

    path('jugarUser', views.acceso_trivia, name='acceso'),

    path('jugarUserr', views.acceso_trivia_test, name='acceso_test'),
    path('configuraciones', views.configuraciones, name='configuraciones'),


    path('jugar/trivia/<int:Trivia_id>/user', views.jugarTriviaUsuario, name='jugarTriviaUsuario'),
    path('test23/<int:Trivia_id>', views.funcion, name='o'),

    path('trivia/<int:Trivia_id>/pregunta/<int:pregunta_num>/', views.pregunta, name='pregunta'),
    path('compiler', views.compiler, name='compiler'),
    path('model', views.asdfghj, name='asdfghj'),
    path('nuevo', views.nuevo_test, name='nuevo'),
    path('runcode', views.runcode, name='runcode'),
    path('game', views.start_game, name='start_game'),
    path('resultado', views.resultado, name='resultado'),

    
    path('compilador', views.compile_view, name="Compilador"),
    path('salidaCompilador', views.execute_code, name="SalidaCompilador"),
 
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)