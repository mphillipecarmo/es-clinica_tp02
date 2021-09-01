from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FormLogin, FormFuncionario, FormFuncionario1, FormPaciente
from django.db.models import Max
from .models import *
from django.contrib import messages
from consultas.models import Endereco, Agendamento
import pdb
import hashlib


def login(request):
    if request.method == 'POST':
        form = FormLogin(request.POST)
        #pdb.set_trace()
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            
            if(len(Funcionario.objects.filter(email=email,senhaHash=senha)) == 1):
                request.session['emailFuncionario'] = email 
                request.session['senhaHash'] = senha
                return redirect('/gerenciamento')
            else:
                messages.error(request, "Email ou senha incorretos.")
                return render(request, 'login.html', {})
            
            pdb.set_trace()
            
    elif request.method == 'GET':
        return render(request, 'login.html', {})
        
def logout(request):
    del request.session['emailFuncionario']
    del request.session['senhaHash']
    return redirect('/')
        
def gerenciamento(request):
    try:
        emailFuncionario = request.session['emailFuncionario']
        senhaHash = request.session['senhaHash']
        
        funcionario = Funcionario.objects.filter(email=emailFuncionario,senhaHash=senhaHash)    
        
        if(len(Medico.objects.filter(email=emailFuncionario,senhaHash=senhaHash)) == 1):
            medico = True
        else:
            medico = False
        
        context = {
            'funcionario': funcionario,
            'medico' : medico
        }
        
        #pdb.set_trace()
        
        return render(request, 'gerenciamento.html', context)
    except KeyError:
        messages.error(request, "Essa é uma área administrativa restrita. Por favor, faça login com sua conta")
        return render(request, 'login.html', {})
    

def cadastrarFuncionario(request):
    try:
        emailFuncionario = request.session['emailFuncionario']
        senhaHash = request.session['senhaHash']
        funcionario = Funcionario.objects.filter(email=emailFuncionario,senhaHash=senhaHash)
        
        context = {
            'funcionario': funcionario,
        }
        if request.method == 'POST':
            if (request.POST['etapa'] == '1'):
                form = FormFuncionario1(request.POST)
                if form.is_valid():
                    cep = form.cleaned_data['cep']
                    form2 = {
                        'nome' : form.cleaned_data['nome'],
                        'email' : form.cleaned_data['email'],
                        'telefone' : form.cleaned_data['telefone'],
                        'dataContrato' : request.POST['dataContrato'],
                        'salario' : form.cleaned_data['salario'],
                        'senha' : form.cleaned_data['senha'],
                        'senhaConf' : form.cleaned_data['senhaConf'],
                        'medico' : form.cleaned_data['medico'],
                        'especialidade' : form.cleaned_data['especialidade'],
                        'crm' : form.cleaned_data['crm']
                    }
                    endereco = Endereco.objects.filter(cep=cep)
                    if(len(endereco) == 1):
                        context = {
                        'logradouro' : endereco[0].logradouro,
                        'bairro' : endereco[0].bairro,
                        'estado' : endereco[0].estado,
                        'cidade' : endereco[0].cidade,
                        'cep' : endereco[0].cep,
                        'form' : form2
                        }
                        return render(request, 'cadastro/funcionario2.html', context)
                    else:
                        context = {
                            'form': form2,
                            'cep' : form.cleaned_data['cep']
                        }
                        messages.warning(request, "CEP não encontrado. Preencha os campos restantes:")
                        return render(request, 'cadastro/funcionario2.html', context)
                    #pdb.set_trace()
            elif (request.POST['etapa'] == '2'):
                #pdb.set_trace()
                form = FormFuncionario(request.POST)
                if form.is_valid():
                    nome = form.cleaned_data['nome']
                    email = form.cleaned_data['email']
                    telefone = form.cleaned_data['telefone']
                    dataContrato = form.cleaned_data['dataContrato']
                    salario = form.cleaned_data['salario']
                    senha = form.cleaned_data['senha']
                    senhaConf = form.cleaned_data['senhaConf']
                    cep = form.cleaned_data['cep']
                    logradouro = form.cleaned_data['logradouro']
                    bairro = form.cleaned_data['bairro']
                    cidade = form.cleaned_data['cidade']
                    estado = form.cleaned_data['estado']
                    medico = form.cleaned_data['medico']
                    especialidade = form.cleaned_data['especialidade']
                    crm = form.cleaned_data['crm']
                    
                    if(medico == 'sim' and (crm == '' or especialidade == '')):
                        messages.error(request, "Não foram informados o CRM e/ou especialidade do Médico")
                        return render(request, 'cadastro/funcionario.html', {})
                    
                    elif(senha != senhaConf):
                        messages.error(request, "A senha e confirmação de senha não correspondem")
                        return render(request, 'cadastro/funcionario.html', {})
                    else:    
                        try:
                            codigo = Pessoa.objects.aggregate(Max('codigo'))['codigo__max'] + 1
                        except TypeError:
                            codigo = 1
                        
                        
                        if(medico == 'sim'):
                            medico = Medico(crm=crm, especialidade=especialidade, codigo=codigo, nome=nome, email=email, telefone=telefone, dataContrato=dataContrato, 
                            salario=salario, senhaHash=senha, cep=cep, logradouro=logradouro, bairro=bairro, cidade=cidade, estado=estado)
                            medico.save()
                            messages.success(request, "Médico cadastrado com sucesso!")
                        else:
                            funcionario = Funcionario(codigo=codigo, nome=nome, email=email, telefone=telefone, dataContrato=dataContrato, 
                            salario=salario, senhaHash=senha, cep=cep, logradouro=logradouro, bairro=bairro, cidade=cidade, estado=estado)
                            funcionario.save()
                            messages.success(request, "Funcionário cadastrado com sucesso!")
                        return render(request, 'cadastro/funcionario.html', context)
                else:
                    messages.error(request, form.errors)
                    return render(request, 'cadastro/funcionario.html', context)
                    #pdb.set_trace()
        elif request.method == 'GET':
            return render(request, 'cadastro/funcionario.html', context)
        
    except KeyError:
        messages.error(request, "Essa é uma área administrativa restrita. Por favor, faça login com sua conta")
        return render(request, 'login.html', {})
        
def cadastrarPaciente(request):
    try:
        emailFuncionario = request.session['emailFuncionario']
        senhaHash = request.session['senhaHash']
        
        funcionario = Funcionario.objects.filter(email=emailFuncionario,senhaHash=senhaHash)
        
        context = {
            'funcionario': funcionario,
        }
        
        if request.method == 'POST':
            form = FormPaciente(request.POST)
            if form.is_valid():
                nome = form.cleaned_data['nome']
                email = form.cleaned_data['email']
                telefone = form.cleaned_data['telefone']
                peso = form.cleaned_data['peso']
                altura = form.cleaned_data['altura']
                tipoSanguineo = form.cleaned_data['tipoSanguineo']
                cep = form.cleaned_data['cep']
                logradouro = form.cleaned_data['logradouro']
                bairro = form.cleaned_data['bairro']
                cidade = form.cleaned_data['cidade']
                estado = form.cleaned_data['estado']
                
                try:
                    codigo = Pessoa.objects.aggregate(Max('codigo'))['codigo__max'] + 1
                except TypeError:
                    codigo = 1
                
                paciente = Paciente(codigo=codigo, nome=nome, email=email, telefone=telefone, peso=peso, altura=altura, 
                tipoSanguineo=tipoSanguineo, cep=cep, logradouro=logradouro, bairro=bairro, cidade=cidade, estado=estado)
                paciente.save()
                
                messages.success(request, "Paciente cadastrado com sucesso!")
                return render(request, 'cadastro/paciente.html', context)
            else:
                messages.error(request, form.errors)
                return render(request, 'cadastro/paciente.html', context)
                #pdb.set_trace()
        elif request.method == 'GET':
            return render(request, 'cadastro/paciente.html', context)
        
    except KeyError:
        messages.error(request, "Essa é uma área administrativa restrita. Por favor, faça login com sua conta")
        return render(request, 'login.html', {})

def listarFuncionarios(request):
    try:
        emailFuncionario = request.session['emailFuncionario']
        senhaHash = request.session['senhaHash']
        
        funcionario = Funcionario.objects.filter(email=emailFuncionario,senhaHash=senhaHash)
        
        
        
        funcionarios = Funcionario.objects.all()
        
        funcionariosNaoMedicos = []
        
        for f in funcionarios:
            if (len(Medico.objects.filter(codigo=f.codigo)) == 0):
                funcionariosNaoMedicos.append(f)
                
        
        medicos = Medico.objects.all()
        
        context = {
            'funcionarios': funcionariosNaoMedicos,
            'funcionario': funcionario,
            'medicos' : medicos,
        }
        return render(request, 'listagem/funcionarios.html', context)
    except KeyError:
        messages.error(request, "Essa é uma área administrativa restrita. Por favor, faça login com sua conta")
        return render(request, 'login.html', {})
    
def listarPacientes(request):
    try:
        emailFuncionario = request.session['emailFuncionario']
        senhaHash = request.session['senhaHash']
        
        funcionario = Funcionario.objects.filter(email=emailFuncionario,senhaHash=senhaHash)
        
        pacientes = Paciente.objects.all()
        context = {
            'pacientes': pacientes,
            'funcionario': funcionario,
        }
        return render(request, 'listagem/pacientes.html', context)
    except KeyError:
        messages.error(request, "Essa é uma área administrativa restrita. Por favor, faça login com sua conta")
        return render(request, 'login.html', {})
    
def listarEnderecos(request):
    try:
        emailFuncionario = request.session['emailFuncionario']
        senhaHash = request.session['senhaHash']
        
        funcionario = Funcionario.objects.filter(email=emailFuncionario,senhaHash=senhaHash)
        
        enderecos = Endereco.objects.all()
        context = {
            'enderecos': enderecos,
            'funcionario': funcionario,
        }
        return render(request, 'listagem/enderecos.html', context)
    except KeyError:
        messages.error(request, "Essa é uma área administrativa restrita. Por favor, faça login com sua conta")
        return render(request, 'login.html', {})
    
def listarAgendamentos(request):
    try:
        emailFuncionario = request.session['emailFuncionario']
        senhaHash = request.session['senhaHash']
        
        funcionario = Funcionario.objects.filter(email=emailFuncionario,senhaHash=senhaHash)
        
        agendamentos = Agendamento.objects.all()
        
        reservas = []
        
        for a in agendamentos:
            reserva = {}
            reserva['codigo'] = a.codigo
            reserva['data'] = a.data
            reserva['horario'] = a.horario
            reserva['nome'] = a.nome
            reserva['email'] = a.email
            reserva['telefone'] = a.telefone
            reserva['nomeMedico'] = Medico.objects.filter(codigo=a.codigoMedico)[0].nome
            reserva['especialidade'] = Medico.objects.filter(codigo=a.codigoMedico)[0].especialidade
            reservas.append(reserva)
        
        context = {
            'agendamentos': reservas,
            'funcionario': funcionario,
        }
        return render(request, 'listagem/agendamentos.html', context)
    except KeyError:
        messages.error(request, "Essa é uma área administrativa restrita. Por favor, faça login com sua conta")
        return render(request, 'login.html', {})
