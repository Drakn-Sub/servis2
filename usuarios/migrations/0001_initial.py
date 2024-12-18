# Generated by Django 5.1.3 on 2024-11-15 22:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(max_length=15, unique=True)),
                ('tipo_usuario', models.CharField(choices=[('cliente', 'Cliente'), ('trabajador', 'Trabajador')], default='cliente', max_length=10)),
                ('password', models.CharField(default='temporary_password', max_length=128)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='usuarios.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='usuarios.usuarios')),
                ('archivo_cv', models.FileField(blank=True, null=True, upload_to='upload_cv/')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(default='sin titulo', max_length=150)),
                ('descripcion', models.TextField()),
                ('creado_en', models.DateTimeField(auto_now_add=True, null=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.categoriaservicio')),
                ('trabajador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service', to='usuarios.usuarios')),
            ],
        ),
    ]
