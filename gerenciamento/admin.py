from django.contrib import admin
from .models import *

from consultas.models import Endereco, Agendamento

# Register your models here.

class PessoaAdmin(admin.ModelAdmin):
    list_display = ('codigo','nome', 'email','telefone','cep','logradouro','bairro','cidade','estado')

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('codigo','nome', 'email','telefone','cep','logradouro','bairro','cidade','estado','dataContrato', 'salario')
    
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('codigo','nome', 'email','telefone','cep','logradouro','bairro','cidade','estado','dataContrato', 'salario','crm','especialidade')

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('codigo','nome', 'email','telefone','cep','logradouro','bairro','cidade','estado','peso','altura','tipoSanguineo')
    
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('cep','logradouro','bairro','cidade','estado')
    
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('codigo','data', 'horario','nome','email','telefone','codigoMedico')
    
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Medico,MedicoAdmin)
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Agendamento, AgendamentoAdmin)