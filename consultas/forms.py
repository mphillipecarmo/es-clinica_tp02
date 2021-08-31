from django import forms
from .models import *

class FormEndereco(forms.Form):
    cep = forms.CharField()
    logradouro = forms.CharField()
    bairro = forms.CharField()
    cidade = forms.CharField()
    estado = forms.CharField()

class FormAgendamento(forms.Form):
    especialidade = forms.CharField()
    medico = forms.CharField()
    data = forms.DateField()
    horario = forms.CharField()
    nome = forms.CharField()
    email = forms.CharField()
    telefone = forms.CharField()

class FormLogin(forms.Form):
    email = forms.CharField()
    senha = forms.CharField()