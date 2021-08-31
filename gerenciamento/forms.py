from django import forms
from .models import *

class FormFuncionario1(forms.Form):
    nome = forms.CharField()
    email = forms.CharField()
    telefone = forms.CharField()
    dataContrato = forms.DateField()
    salario = forms.CharField()
    senha = forms.CharField()
    senhaConf = forms.CharField()
    cep = forms.CharField()
    medico = forms.CharField()
    especialidade = forms.CharField(required=False)
    crm = forms.CharField(required=False)

class FormFuncionario(forms.Form):
    nome = forms.CharField()
    email = forms.CharField()
    telefone = forms.CharField()
    dataContrato = forms.DateField()
    salario = forms.CharField()
    senha = forms.CharField()
    senhaConf = forms.CharField()
    cep = forms.CharField()
    logradouro = forms.CharField()
    bairro = forms.CharField()
    cidade = forms.CharField()
    estado = forms.CharField()
    medico = forms.CharField()
    especialidade = forms.CharField(required=False)
    crm = forms.CharField(required=False)
    

class FormLogin(forms.Form):
    email = forms.CharField()
    senha = forms.CharField()
    
class FormPaciente(forms.Form):
    nome = forms.CharField()
    email = forms.CharField()
    telefone = forms.CharField()
    cep = forms.CharField()
    logradouro = forms.CharField()
    bairro = forms.CharField()
    cidade = forms.CharField()
    estado = forms.CharField()
    peso = forms.CharField()
    altura = forms.CharField()
    tipoSanguineo = forms.CharField()