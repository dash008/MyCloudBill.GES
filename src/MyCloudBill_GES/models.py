from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Distribucion(models.Model):
	financiero = models.IntegerField()
	sugiro = models.IntegerField()
	vivienda = models.IntegerField()
	mp = models.IntegerField()
	eps = models.IntegerField()
	eme= models.IntegerField()
	homecare= models.IntegerField()
	seguros = models.IntegerField()
	solidaridad = models.IntegerField()
	vida_en_plenitud = models.IntegerField()
	centro_vacacional= models.IntegerField()
	agencia_viajes= models.IntegerField()
	gremial = models.IntegerField()

class Empresa(models.Model):	
	nombre = models.CharField(max_length = 50)
	def __str__(self):
		return u'{0}'.format(self.nombre)
	

class Negociacion(models.Model):
	date = models.DateField(default=datetime.now, blank=True)
	fecha_negociacion = models.CharField(max_length=30)
	proovedor = models.CharField(max_length = 30)
	tiempo_de_servicio = models.IntegerField()
	cargototal = models.IntegerField()
	cargoinicial = models.IntegerField()
	cargomeslineabase = models.IntegerField()
	estado = models.CharField(max_length=30,default = 'actual')		


class Solicitud(models.Model):
	
	plataforma = models.CharField(max_length=30)
	sistemaoperativo = models.CharField(max_length=100)
	basededatos = models.CharField(max_length=30)
	procesador =models.CharField(max_length=30)
	procesamiento = models.CharField(max_length=30)
	numeroprocesadores = models.CharField(max_length = 30)
	memoria = models.CharField(max_length=30)
	almacenamiento = models.CharField(max_length=30)
	backupimagenes = models.CharField(max_length=30)
	estado = models.CharField(max_length= 30)
	user_id = models.CharField(max_length= 30)
	tiempodeuso = models.CharField(max_length= 30)
	cantidaddeusuarios = models.CharField(max_length=5)
	justificacion = models.TextField(max_length=1000)
	id_distribucion = models.OneToOneField(Distribucion,related_name= "distribuciones")
	negociacion = models.ForeignKey(Negociacion, on_delete=models.CASCADE)
	empresas = models.ManyToManyField(Empresa, blank=True,related_name="empresas")
	porcentaje_de_aprobacion_ti = models.FloatField(null= True,default=0.0)
	porcentaje_de_aprobacion_infra = models.FloatField(null=True, default=0.0)
	fechaaprobacion = models.DateField(blank=True, null= True,default = datetime.now)

class RecursosCRA(models.Model):
	solicitud = models.OneToOneField(Solicitud,related_name="recursos_solicitud",on_delete=models.CASCADE, primary_key=True,) 
	procesador= models.CharField(max_length = 30)
	numeroprocesadores = models.IntegerField()
	memoria = models.CharField(max_length = 30)
	almacenamiento = models.CharField(max_length=30)



class Factura(models.Model):
	numero = models.IntegerField(null = True)
	solicitud = models.ForeignKey(Solicitud,related_name="facturas_solicitud",on_delete = models.CASCADE, null = True,)
	periodo = models.TextField(max_length = 255,null =True)
	financiero = models.IntegerField(null = True)
	sugiro = models.IntegerField(null = True)
	vivienda = models.IntegerField(null = True)
	mp = models.IntegerField(null = True)
	eps = models.IntegerField(null = True)
	eme= models.IntegerField(null = True)
	homecare= models.IntegerField(null = True)
	seguros = models.IntegerField(null = True)
	solidaridad = models.IntegerField(null = True)
	vida_en_plenitud = models.IntegerField(null = True)
	centro_vacacional= models.IntegerField(null = True)
	agencia_viajes= models.IntegerField(null = True)
	gremial = models.IntegerField(null = True)

class NuevosRecursos(models.Model):
	solicitud = models.ForeignKey(Solicitud,related_name="nuevorecurso_solicitud",on_delete = models.CASCADE, null = True,)
	nuevo_recurso = models.CharField(max_length = 30)
	tiempo_de_uso = models.CharField(max_length = 30)
	fechasolicitud = models.DateField(null = True)
	factura = models.ForeignKey(Factura,related_name="factura_nuevorecrs",on_delete=models.CASCADE,null=True,)

	




class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User,related_name= "Users")

    # The additional attributes we wish to include.
    rol = models.CharField(max_length=30)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
	


class Busqueda(models.Model):
	search_query = models.CharField(max_length=10)


class TiempoReal(models.Model):
	fechainicio = models.DateField(default=datetime.now, blank=True)
	fechafin = models.DateField(blank = True)
	solicitud = models.OneToOneField(Solicitud,on_delete=models.CASCADE, blank = True, null = True)

class AprobacionTI(models.Model):
	solicitud = models.OneToOneField(Solicitud,related_name="aprobacion_ti_solicitud",on_delete = models.CASCADE, null = True,)
	financiero = models.IntegerField(default=0)
	sugiro = models.IntegerField(default=0)
	vivienda = models.IntegerField(default=0)
	mp = models.IntegerField(default=0)
	eps = models.IntegerField(default=0)
	eme= models.IntegerField(default=0)
	homecare= models.IntegerField(default=0)
	seguros = models.IntegerField(default=0)
	solidaridad = models.IntegerField(default=0)
	vida_en_plenitud = models.IntegerField(default=0)
	centro_vacacional= models.IntegerField(default=0)
	agencia_viajes= models.IntegerField(default=0)
	gremial = models.IntegerField(default=0)

class AprobacionInfra(models.Model):
	solicitud = models.OneToOneField(Solicitud,related_name="aprobacion_infra_solicitud",on_delete = models.CASCADE, null = True,)
	financiero = models.IntegerField(default=0)
	sugiro = models.IntegerField(default=0)
	vivienda = models.IntegerField(default=0)
	mp = models.IntegerField(default=0)
	eps = models.IntegerField(default=0)
	eme= models.IntegerField(default=0)
	homecare= models.IntegerField(default=0)
	seguros = models.IntegerField(default=0)
	solidaridad = models.IntegerField(default=0)
	vida_en_plenitud = models.IntegerField(default=0)
	centro_vacacional= models.IntegerField(default=0)
	agencia_viajes= models.IntegerField(default=0)
	gremial = models.IntegerField(default=0)

		