from django.db import models

class Pessoa(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.TextField()
    email = models.TextField()
    telefone = models.TextField()
    cep = models.TextField()
    logradouro = models.TextField()
    bairro = models.TextField()
    cidade = models.TextField()
    estado = models.TextField()

class Funcionario(Pessoa):
    dataContrato = models.DateField()
    salario = models.FloatField()
    senhaHash = models.TextField()
    #codigo = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    
class Paciente(Pessoa):
    peso = models.FloatField()
    altura = models.FloatField()
    tipoSanguineo = models.TextField()
    #codigo = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    
class Medico(Funcionario):
    especialidade = models.TextField()
    crm = models.TextField()
    