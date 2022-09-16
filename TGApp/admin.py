from django.contrib import admin
from .models import Pregunta, Trivia, Admin

# Register your models here.

admin.site.register(Pregunta)
admin.site.register(Trivia)
admin.site.register(Admin)