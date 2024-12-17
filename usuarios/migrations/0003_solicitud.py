# Generated by Django 5.1.3 on 2024-12-15 00:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_service_calificacion_service_cliente_solicitante_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.TextField()),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Aceptado', 'Aceptado'), ('Rechazado', 'Rechazado')], max_length=10)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes_cliente', to='usuarios.cliente')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.service')),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes_trabajador', to='usuarios.trabajador')),
            ],
        ),
    ]