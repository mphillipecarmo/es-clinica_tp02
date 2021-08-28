from django.db import models

class Endereco(models.Model):
    cep = models.TextField(primary_key=True)
    logradouro = models.TextField()
    bairro = models.TextField()
    cidade = models.TextField()
    estado = models.TextField()

class Agendamento(models.Model):
    codigo = models.IntegerField(primary_key=True)
    data = models.DateField()
    horario = models.TimeField()
    nome = models.TextField()
    email = models.TextField()
    telefone = models.TextField()
    codigoMedico = models.IntegerField()