from django import forms
from .models import *

class FormEndereco(forms.Form):
    cep = forms.CharField()
    logradouro = forms.CharField()
    bairro = forms.CharField()
    cidade = forms.CharField()
    estado = forms.CharField()


class FormLogin(forms.Form):
    email = forms.CharField()
    senha = forms.CharField()