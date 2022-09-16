from pyexpat import model
from django import forms
from .models import Pregunta, Trivia, Admin

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = '__all__'

# class RegistroFormulario(UserCreationForm):
#     #proporciona 3 parametros
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)

#     class Meta:
#         model = User

#         fields = [
#             'first_name',
#             'last_name',
#             'username',
#             'email',
#             'password1',
#             'password2',
#         ]