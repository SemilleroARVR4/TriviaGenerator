from django.urls import path
from . import views

urlpatterns = [
    # 'url' 'nombre de la funcion en views' 'titulo'
    path('', views.inicio, name='inicio'),
    # path('registro', views.registro, name='registro'),
    # path('login', views.loginView, name='login'),
    # path('logout', views.logoutView, name='logout'),
    # path('InicioUsuario', views.InicioUsuario, name='InicioUsuario'),
    # path('resultado/<int:pregunta_respondida_pk>/', views.resultado_pregunta, name='resultado'),
    # path('tablero', views.tablero, name='tablero'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('crear', views.crear, name='crear'),
    # path('crear/agregar', views.crearPregunta, name='crearPregunta'),
    path('crear/agregar/<int:Trivia_id>/', views.crearPregunta, name='crearPregunta'),  #aqui dirige el index
    path('crear/agregar/nuevo', views.crearNuevaPregunta, name='crearNuevaPregunta'),

    path('crear/editar', views.editarPregunta, name='editarPregunta'),
    path('jugar', views.jugar, name='jugar'),
       
]