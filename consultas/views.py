from django.shortcuts import render
from .forms import FormEndereco,FormLogin,FormAgendamento
from django.contrib import messages
from .models import *
from django.db.models import Max
from gerenciamento.models import Medico

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

def agendamento(request):
    if request.method == 'POST':
        form = FormAgendamento(request.POST)
        #pdb.set_trace()
        if form.is_valid():
            especialidade = form.cleaned_data['especialidade']
            medico = form.cleaned_data['medico']
            data = form.cleaned_data['data']
            horario = form.cleaned_data['horario']
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            telefone = form.cleaned_data['telefone']
            
            try:
                codigo = Agendamento.objects.aggregate(Max('codigo'))['codigo__max'] + 1
            except TypeError:
                codigo = 1
            
            agendamento = Agendamento(codigo=codigo,codigoMedico=medico, data=data, horario=horario, nome=nome,email=email,telefone=telefone)
            agendamento.save()
            
            messages.success(request, "Agendamento efetuado com sucesso!")
            return render(request, 'agendamento6.html', {})
        else:
            messages.error(request, form.errors)
            return render(request, 'agendamento.html', {})
    elif request.method == 'GET':
        try:
            especialidade = request.GET['especialidade']
            try:
                medico = request.GET['medico']
                try:
                    data = request.GET['data']
                    try:
                        horario = request.GET['horario']
                        context = {
                            'especialidade': especialidade,
                            'medico' : Medico.objects.filter(codigo=medico)[0],
                            'data' : data,
                            'horario' : horario
                        }
                        return render(request, 'agendamento5.html', context)
                    except KeyError:
                    
                        horariosLivres = []
                        horariosOcupados = []
                        agendamentos = Agendamento.objects.filter(codigoMedico=medico, data=data)
                        for a in agendamentos:
                            horariosOcupados.append(a.horario)
                        
                        for i in range(8,18):
                            if str(i) not in horariosOcupados:
                                horariosLivres.append(str(i))
                        #pdb.set_trace()
                        context = {
                            'especialidade': especialidade,
                            'medico' : Medico.objects.filter(codigo=medico)[0],
                            'data' : data,
                            'horariosLivres' : horariosLivres,
                        }
                        return render(request, 'agendamento4.html', context)
                except KeyError:
                    context = {
                        'especialidade': especialidade,
                        'medico' : Medico.objects.filter(codigo=medico)[0]
                    }
                    return render(request, 'agendamento3.html', context)
            except KeyError:
                medicos = Medico.objects.filter(especialidade=especialidade)
                context = {
                    'especialidade': especialidade,
                    'medicos' : medicos
                }
                return render(request, 'agendamento2.html', context)
        except KeyError:
            especialidades = []
            medicos = Medico.objects.all()
            for m in medicos:
                if m.especialidade not in especialidades:
                    especialidades.append(m.especialidade)
            context = {
                'especialidades' : especialidades
            }
            return render(request, 'agendamento.html', context)