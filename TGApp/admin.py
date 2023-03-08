from django.contrib import admin
from .models import Pregunta, Trivia, PreguntaQuiz, ElegirRespuesta, PreguntasRespondidasTrivia, QuizUsuarioTrivia, UsuarioTrivia, test_file, user_acceso, user_inicio
from .forms import ElegirInLineFormset


# Register your models here.

admin.site.register(Pregunta)
admin.site.register(Trivia)
admin.site.register(UsuarioTrivia)
admin.site.register(test_file)
admin.site.register(user_acceso)
admin.site.register(user_inicio)


#VIDEO

class ElegirRespuestaInLine(admin.TabularInline):
    
    formset = ElegirInLineFormset
    model = ElegirRespuesta
    can_delete = False
    max_num = ElegirRespuesta.MAXIMO_RESPUESTA
    min_num = ElegirRespuesta.MAXIMO_RESPUESTA


class PreguntaAdmin(admin.ModelAdmin):
    model = PreguntaQuiz
    inlines = (ElegirRespuestaInLine, )
    list_display = ['texto', ]
    search_fields = ['texto', 'preguntas__texto']

class PreguntasRespondidasAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje_obtenido']

    class Meta:
        model = PreguntasRespondidasTrivia

admin.site.register(PreguntasRespondidasTrivia)
admin.site.register(PreguntaQuiz, PreguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(QuizUsuarioTrivia)



