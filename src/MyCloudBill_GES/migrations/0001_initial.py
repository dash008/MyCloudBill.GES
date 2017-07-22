# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AprobacionInfra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('financiero', models.IntegerField(default=0)),
                ('sugiro', models.IntegerField(default=0)),
                ('vivienda', models.IntegerField(default=0)),
                ('mp', models.IntegerField(default=0)),
                ('eps', models.IntegerField(default=0)),
                ('eme', models.IntegerField(default=0)),
                ('homecare', models.IntegerField(default=0)),
                ('seguros', models.IntegerField(default=0)),
                ('solidaridad', models.IntegerField(default=0)),
                ('vida_en_plenitud', models.IntegerField(default=0)),
                ('centro_vacacional', models.IntegerField(default=0)),
                ('agencia_viajes', models.IntegerField(default=0)),
                ('gremial', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AprobacionTI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('financiero', models.IntegerField(default=0)),
                ('sugiro', models.IntegerField(default=0)),
                ('vivienda', models.IntegerField(default=0)),
                ('mp', models.IntegerField(default=0)),
                ('eps', models.IntegerField(default=0)),
                ('eme', models.IntegerField(default=0)),
                ('homecare', models.IntegerField(default=0)),
                ('seguros', models.IntegerField(default=0)),
                ('solidaridad', models.IntegerField(default=0)),
                ('vida_en_plenitud', models.IntegerField(default=0)),
                ('centro_vacacional', models.IntegerField(default=0)),
                ('agencia_viajes', models.IntegerField(default=0)),
                ('gremial', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Busqueda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('search_query', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Distribucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('financiero', models.IntegerField()),
                ('sugiro', models.IntegerField()),
                ('vivienda', models.IntegerField()),
                ('mp', models.IntegerField()),
                ('eps', models.IntegerField()),
                ('eme', models.IntegerField()),
                ('homecare', models.IntegerField()),
                ('seguros', models.IntegerField()),
                ('solidaridad', models.IntegerField()),
                ('vida_en_plenitud', models.IntegerField()),
                ('centro_vacacional', models.IntegerField()),
                ('agencia_viajes', models.IntegerField()),
                ('gremial', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('numero', models.IntegerField(null=True)),
                ('periodo', models.CharField(max_length=30, null=True)),
                ('financiero', models.IntegerField(null=True)),
                ('sugiro', models.IntegerField(null=True)),
                ('vivienda', models.IntegerField(null=True)),
                ('mp', models.IntegerField(null=True)),
                ('eps', models.IntegerField(null=True)),
                ('eme', models.IntegerField(null=True)),
                ('homecare', models.IntegerField(null=True)),
                ('seguros', models.IntegerField(null=True)),
                ('solidaridad', models.IntegerField(null=True)),
                ('vida_en_plenitud', models.IntegerField(null=True)),
                ('centro_vacacional', models.IntegerField(null=True)),
                ('agencia_viajes', models.IntegerField(null=True)),
                ('gremial', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Negociacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('fecha_negociacion', models.CharField(max_length=30)),
                ('proovedor', models.CharField(max_length=30)),
                ('tiempo_de_servicio', models.IntegerField()),
                ('cargototal', models.IntegerField()),
                ('cargoinicial', models.IntegerField()),
                ('cargomeslineabase', models.IntegerField()),
                ('estado', models.CharField(max_length=30, default='actual')),
            ],
        ),
        migrations.CreateModel(
            name='NuevosRecursos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nuevo_recurso', models.CharField(max_length=30)),
                ('tiempo_de_uso', models.CharField(max_length=30)),
                ('fechasolicitud', models.DateField(null=True)),
                ('factura', models.ForeignKey(related_name='factura_nuevorecrs', null=True, to='MyCloudBill_GES.Factura')),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('plataforma', models.CharField(max_length=30)),
                ('sistemaoperativo', models.CharField(max_length=100)),
                ('basededatos', models.CharField(max_length=30)),
                ('procesador', models.CharField(max_length=30)),
                ('procesamiento', models.CharField(max_length=30)),
                ('numeroprocesadores', models.CharField(max_length=30)),
                ('memoria', models.CharField(max_length=30)),
                ('almacenamiento', models.CharField(max_length=30)),
                ('backupimagenes', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=30)),
                ('user_id', models.CharField(max_length=30)),
                ('tiempodeuso', models.CharField(max_length=30)),
                ('cantidaddeusuarios', models.CharField(max_length=5)),
                ('justificacion', models.TextField(max_length=1000)),
                ('porcentaje_de_aprobacion_ti', models.FloatField(null=True, default=0.0)),
                ('porcentaje_de_aprobacion_infra', models.FloatField(null=True, default=0.0)),
                ('fechaaprobacion', models.DateField(null=True, blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='TiempoReal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('fechainicio', models.DateField(blank=True, default=datetime.datetime.now)),
                ('fechafin', models.DateField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('rol', models.CharField(max_length=30)),
                ('empresa', models.ForeignKey(to='MyCloudBill_GES.Empresa')),
                ('user', models.OneToOneField(related_name='Users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecursosCRA',
            fields=[
                ('solicitud', models.OneToOneField(related_name='recursos_solicitud', to='MyCloudBill_GES.Solicitud', serialize=False, primary_key=True)),
                ('procesador', models.CharField(max_length=30)),
                ('numeroprocesadores', models.IntegerField()),
                ('memoria', models.CharField(max_length=30)),
                ('almacenamiento', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='tiemporeal',
            name='solicitud',
            field=models.OneToOneField(null=True, blank=True, to='MyCloudBill_GES.Solicitud'),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='empresas',
            field=models.ManyToManyField(blank=True, to='MyCloudBill_GES.Empresa', related_name='empresas'),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='id_distribucion',
            field=models.OneToOneField(related_name='distribuciones', to='MyCloudBill_GES.Distribucion'),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='negociacion',
            field=models.ForeignKey(to='MyCloudBill_GES.Negociacion'),
        ),
        migrations.AddField(
            model_name='nuevosrecursos',
            name='solicitud',
            field=models.ForeignKey(related_name='nuevorecurso_solicitud', null=True, to='MyCloudBill_GES.Solicitud'),
        ),
        migrations.AddField(
            model_name='factura',
            name='solicitud',
            field=models.ForeignKey(related_name='facturas_solicitud', null=True, to='MyCloudBill_GES.Solicitud'),
        ),
        migrations.AddField(
            model_name='aprobacionti',
            name='solicitud',
            field=models.OneToOneField(related_name='aprobacion_ti_solicitud', null=True, to='MyCloudBill_GES.Solicitud'),
        ),
        migrations.AddField(
            model_name='aprobacioninfra',
            name='solicitud',
            field=models.OneToOneField(related_name='aprobacion_infra_solicitud', null=True, to='MyCloudBill_GES.Solicitud'),
        ),
    ]
