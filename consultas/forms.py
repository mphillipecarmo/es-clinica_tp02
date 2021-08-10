from django import forms
from .models import *

class FormEndereco(forms.Form):
    cep = forms.CharField()
    logradouro = forms.CharField()
    bairro = forms.CharField()
    cidade = forms.CharField()
    estado = forms.CharField()
