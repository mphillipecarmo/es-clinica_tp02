# Generated by Django 3.0.5 on 2021-08-28 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0002_auto_20210825_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamento',
            name='horario',
            field=models.TextField(),
        ),
    ]
