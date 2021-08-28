from django.shortcuts import render
from .forms import FormEndereco,FormLogin
from django.contrib import messages
from .models import *

import pdb

# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def galeria(request):
    return render(request, 'galeria.html', {})

def cadastrarEndereco(request):
    if request.method == 'POST':
        form = FormEndereco(request.POST)
        #pdb.set_trace()
        if form.is_valid():
            cep = form.cleaned_data['cep']
            logradouro = form.cleaned_data['logradouro']
            bairro = form.cleaned_data['bairro']
            cidade = form.cleaned_data['cidade']
            estado = form.cleaned_data['estado']
            
            endereco = Endereco(cep=cep, logradouro=logradouro, bairro=bairro, cidade=cidade, estado=estado)
            endereco.save()
            
            messages.success(request, "Endereço cadastrado com sucesso!")
            return render(request, 'cadastro/endereco.html', {})
        else:
            messages.error(request, form.errors)
            return render(request, 'cadastro/endereco.html', {})
            #pdb.set_trace()
    elif request.method == 'GET':
        return render(request, 'cadastro/endereco.html', {})
