from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from MyCloudBill_GES.forms import SolicitudForm, SearchForm, UserForm, UserProfileForm, FacturaForm, DistribucionForm, NuevosRecursosForm, NegociacionForm
from MyCloudBill_GES.models import Solicitud, Empresa, Distribucion, UserProfile, Negociacion, RecursosCRA, TiempoReal, AprobacionTI, AprobacionInfra, Factura, NuevosRecursos
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from datetime import datetime, timedelta
import re
import math
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib import colors
cm = 2.54

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.db.models import Q
from django.core.management import call_command
from multiprocessing import Process




def about(request):
	return render(request, "about.html", {})

def features(request):
	return render(request, "features.html", {})

@login_required (login_url='/')
def controlpanel(request):
    user = request.user
    users_in_group_coordinador= Group.objects.get(name="CoordinadorSI").user_set.all()
    users_in_group_arquitecto= Group.objects.get(name="ArqSoluciones").user_set.all()
    users_in_group_jefe_infraestructura= Group.objects.get(name="JefeInfraestructura").user_set.all()
    users_in_group_jefe_ti= Group.objects.get(name="JefeTI").user_set.all()
    users_in_group_lider_infraestructura= Group.objects.get(name="LiderInfraestructura").user_set.all()
    my_group = str(request.user.groups.values_list('name', flat=True))

    if user in users_in_group_coordinador:
        userid = request.user.id
        query_results = Solicitud.objects.filter(user_id = userid).count()
        count_windows = Solicitud.objects.filter(plataforma='Windows').filter(user_id = userid).count()
        count_linux = Solicitud.objects.filter(plataforma='Linux').filter(user_id = userid).count()
        count_Aix = Solicitud.objects.filter(plataforma='Aix').filter(user_id = userid).count()
        count_i5 = Solicitud.objects.filter(plataforma='i5/OS').filter(user_id = userid).count()
        data = \
            [
                int(count_windows),
                int(count_linux),
                int(count_Aix),
                int(count_i5)
            ]
        request.session['cantidad'] = query_results
        return render(request, "cpcoordinadorsi.html", {'query_results':query_results,'data':data,'my_group':my_group})
    elif user in users_in_group_arquitecto:
        query_results = Solicitud.objects.filter(estado = 'EnAprobacionArq').count()
        request.session['cantidad'] = query_results

        count_windows = Solicitud.objects.filter(plataforma = 'Windows').count()
        count_linux = Solicitud.objects.filter(plataforma = 'Linux').count()
        count_Aix = Solicitud.objects.filter(plataforma = 'Aix').count()
        count_i5 = Solicitud.objects.filter(plataforma = 'i5/OS').count()

        count_oracle = Solicitud.objects.filter(basededatos = 'Oracle').count()
        count_sql = Solicitud.objects.filter(basededatos = 'SQL Server').count()
        count_sybase = Solicitud.objects.filter(basededatos = 'SYBASE').count()
        count_iseries = Solicitud.objects.filter(basededatos = 'iSeries DB2').count()

        return render(request, "cparqsoluciones.html", {'query_results':query_results,'count_windows':count_windows,'count_linux':count_linux,'count_Aix':count_Aix,'count_i5':count_i5,'count_oracle':count_oracle,'count_sql':count_sql,'count_iseries':count_iseries,'count_sybase':count_sybase})
    elif user in users_in_group_jefe_infraestructura:
        userid = request.user.id
        query_results = Solicitud.objects.filter(estado = 'EnAprobacion').count()
        count_windows = Solicitud.objects.filter(plataforma='Windows').count()
        count_linux = Solicitud.objects.filter(plataforma='Linux').count()
        count_Aix = Solicitud.objects.filter(plataforma='Aix').count()
        count_i5 = Solicitud.objects.filter(plataforma='i5/OS').count()
        data = \
            [
                int(count_windows),
                int(count_linux),
                int(count_Aix),
                int(count_i5)
            ]
        request.session['cantidad'] = query_results
        return render(request, "cpjefeinfraestructura.html", {'query_results':query_results,'data':data,'my_group':my_group})
    elif user in users_in_group_jefe_ti:
        query_results = Solicitud.objects.filter(estado = 'EnValoracion').count()
        request.session['cantidad'] = query_results
        return render(request, "cpjefeti.html", {'my_group':my_group})
    elif user in users_in_group_lider_infraestructura:
        query_results = Solicitud.objects.filter(estado = 'Aprobado').count()
        request.session['cantidad'] = query_results
        return render(request, "cpliderinfraestructura.html", {'my_group':my_group})

@login_required (login_url='/')
def consultasolicitud(request):

    user = request.user
    users_in_group_coordinador= Group.objects.get(name="CoordinadorSI").user_set.all()
    users_in_group_arquitecto= Group.objects.get(name="ArqSoluciones").user_set.all()
    users_in_group_jefe_infraestructura= Group.objects.get(name="JefeInfraestructura").user_set.all()
    users_in_group_jefe_ti= Group.objects.get(name="JefeTI").user_set.all()
    users_in_group_lider_infraestructura= Group.objects.get(name="LiderInfraestructura").user_set.all()
    group = ""
    #COORDINADOR TI
    if user in users_in_group_coordinador:
        cantidad_solicitudes = request.session.get('cantidad')
        userid = request.user.id
        pendientes = Solicitud.objects.filter(estado = 'EnProcesoCoordinador')
        aprob_arq  = Solicitud.objects.all().exclude(estado= 'EnProcesoCoordinador').exclude(estado= 'cancelado')
        cancelados = Solicitud.objects.filter(estado = 'cancelado')
        group = 'CoordinadorSI'
        return render_to_response( "consultasolicitud.html", {'cantidad_solicitudes':cantidad_solicitudes,'group':group,'pendientes':pendientes,'aprob_arq': aprob_arq,'cancelados': cancelados})

    #ARQUITECTO DE SOLUCIONES
    elif user in users_in_group_arquitecto:
        cantidad_solicitudes = request.session.get('cantidad')
        aprob_arq = Solicitud.objects.filter(estado = 'EnAprobacionArq')
        liberados = Solicitud.objects.filter(estado = 'Liberado')
        group = 'ArqSoluciones'
        return render_to_response( "consultasolicitud.html", {'cantidad_solicitudes':cantidad_solicitudes,'group':group,'aprob_arq':aprob_arq,'liberados':liberados })

    #JEFE INFRAESTRUCTURA
    elif user in users_in_group_jefe_infraestructura:
        #Pedir ID al usuario y rescatar empresa en la que trabaja
        userid = request.user.id
        empresa = UserProfile.objects.get(user = userid).empresa
        cantidad_solicitudes = request.session.get('cantidad')

        #Hace un join con las solicitudes aprobadas y la empresa a que pertenece el usuario quien quiere visualizar
        en_aprobacion = Solicitud.objects.select_related().filter(estado='EnAprobacion').filter(empresas = empresa)
        print("CONSULTA:")
        for item in en_aprobacion:
        	print(item.id)
         #Hace un join con las solicitudes liberadas y la empresa a que pertenece el usuario quien quiere visualizar
        liberados = Solicitud.objects.select_related().filter(estado = 'Liberado').filter(empresas = empresa)
        group = 'JefeInfraestructura'
        return render_to_response( "consultasolicitud.html", {'cantidad_solicitudes':cantidad_solicitudes,'group':group,'en_aprobacion':en_aprobacion,'liberados':liberados})
    #JEFE TI
    elif user in users_in_group_jefe_ti:
        #Pedir ID al usuario y rescatar empresa en la que trabaja
        userid = request.user.id
        empresa = UserProfile.objects.get(user = userid).empresa

        #Hace un join con las solicitudes liberadas y la empresa a que pertenece el usuario quien quiere visualizar
        cantidad_solicitudes = request.session.get('cantidad')
        en_valoracion = Solicitud.objects.select_related().filter(estado = 'EnValoracion').filter(empresas = empresa)
        contabilizados = Solicitud.objects.select_related().filter(estado = 'Contabilizado').filter(empresas = empresa)
        group = 'JefeTI'
        return render_to_response( "consultasolicitud.html", {'cantidad_solicitudes':cantidad_solicitudes,'group':group,'en_valoracion':en_valoracion,'contabilizados':contabilizados})
    #LIDER INFRAESTRUCTURA
    elif user in users_in_group_lider_infraestructura:
        cantidad_solicitudes = request.session.get('cantidad')
        aprobados = Solicitud.objects.filter(estado = 'Aprobado')
        para_pago = Solicitud.objects.filter(estado = 'ParaPago')
        group = 'LiderInfraestructura'
        return render_to_response( "consultasolicitud.html", {'cantidad_solicitudes':cantidad_solicitudes,'group':group,'aprobados':aprobados,'para_pago':para_pago})

@login_required (login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='CoordinadorSI').count() == 1, login_url='/controlpanel')
def eliminarsolicitud(request):    
    #A HTTP POST?
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if 'search_btn' in request.POST:
            if form.is_valid():
                instance = form.save(commit=False)
                searchquery = instance.search_query
                query_results = Solicitud.objects.filter(id = searchquery)
                try:
                    solicitud = Solicitud.objects.get(id = searchquery)
                    request.session['solicitud_encontrada']  = solicitud.id
                    cantidad_solicitudes = request.session['cantidad']
                except:
                    messages.error(request, 'La solicitud buscada no existe!')
                    return render(request, "eliminarsolicitud.html", {'form':form})

                if  str(request.user.id) == solicitud.user_id :
                    return render(request, "eliminarsolicitud.html", {'query_results':query_results,'cantidad_solicitudes':cantidad_solicitudes})
                else:
                    print("El id del usuario es: "+ str(request.user.id)+" y el del usuario asociado a la solicitud es: "+str(solicitud.user_id))

                    return render(request, "eliminarsolicitud.html", {})
        elif 'remove_btn' in request.POST:
            if form.is_valid():
                try:
                    solicitud_instance = Solicitud.objects.get(id = request.session['solicitud_encontrada'])
                    solicitud_instance.estado ='cancelado'
                    solicitud_instance.save()
                    messages.success(request, 'Solicitud cancelada exitosamente!')
                    return render(request, "eliminarsolicitud.html", {'form':form})
                except (KeyError, Solicitud.DoesNotExist):
                    solicitud_instance = None
        else:
                print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = SearchForm()
    return render(request, "eliminarsolicitud.html", {'form':form})

@login_required (login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='CoordinadorSI').count() == 1, login_url='/controlpanel')
def registrosolicitud(request):
    #A HTTP POST?
    my_group = str(request.user.groups.values_list('name', flat=True))
    datos = []
    #Si el metodo es POST y el usuario esta autentificado
    if request.method == 'POST' and request.user.is_authenticated():
        userid = request.user.id
        form = SolicitudForm(request.POST,group = my_group)
        distribucion_form = DistribucionForm(request.POST)
        # Revisar si los formularios son validos
        if form.is_valid() and distribucion_form.is_valid():
            # Guardar la nueva solicitud en la base de datos.
            if 'save_def' in request.POST :
                instance = form.save(commit=False)
                distribucion_instance = distribucion_form.save(commit=False)
                #Sumar la cantidad de empleados en la distribucion de la solicitud, para ver si coincide con lo colocado en la solicitud
                total_cantidad_empleados  =  distribucion_instance.financiero+distribucion_instance.sugiro +distribucion_instance.vivienda +distribucion_instance.mp +distribucion_instance.eps +distribucion_instance.eme +distribucion_instance.homecare +distribucion_instance.seguros +distribucion_instance.solidaridad +distribucion_instance.vida_en_plenitud +distribucion_instance.centro_vacacional +distribucion_instance.agencia_viajes +distribucion_instance.gremial

                if total_cantidad_empleados != int(instance. cantidaddeusuarios):
                    messages.error(request, 'El numero Total de usuarios no coincide con la distribucion')
                    return render(request, 'registrosolicitud.html', {'form': form,'distribucion_form':distribucion_form})
                instance.user_id = userid
                instance.estado= 'EnAprobacionArq'


                distribucion_instance.save()
                instance.id_distribucion_id = distribucion_instance.id
                instance.negociacion = Negociacion.objects.get(estado = 'actual')
                instance.save()
                numero_solicitud = instance.id

                aprobacion_ti = AprobacionTI.objects.create(solicitud = instance)
                aprobacion_infra = AprobacionInfra.objects.create(solicitud = instance)
                #Verificar las empresas que participan en la solicitud mediante la distribucion
                if(distribucion_instance.financiero > 0):
                    empresa = Empresa.objects.get(pk=1)
                    instance.empresas.add(empresa)
                    aprobacion_ti.financiero = -1
                    aprobacion_infra.financiero = -1
                    aprobacion_ti.save()
                    aprobacion_infra.save()
                if(distribucion_instance.eme > 0):
                    empresa_obj = Empresa.objects.get(id=6)

                    print(empresa_obj)
                    instance.empresas.add(empresa_obj)
                    print(instance)
                    aprobacion_ti.eme = -1
                    aprobacion_infra.eme = -1
                    aprobacion_ti.save()
                    aprobacion_infra.save()

                if(distribucion_instance.sugiro > 0):
                    empresa = Empresa.objects.get(pk=2)
                    instance.empresas.add(empresa)
                    aprobacion_ti.sugiro = -1
                    aprobacion_infra.sugiro = -1
                    aprobacion_ti.save()
                    aprobacion_infra.save()
                if(distribucion_instance.vivienda > 0):
                    empresa = Empresa.objects.get(pk=3)
                    instance.empresas.add(empresa)
                    aprobacion_ti.vivienda = -1
                    aprobacion_infra.vivienda = -1
                    aprobacion_ti.save()
                    aprobacion_infra.save()
                if(distribucion_instance.mp > 0):
                    empresa = Empresa.objects.get(pk=4)
                    instance.empresas.add(empresa)
                    aprobacion_ti.mp = -1
                    aprobacion_infra.mp = -1
                    aprobacion_ti.save()
                    aprobacion_infra.save()
                if(distribucion_instance.eps > 0):
                    empresa = Empresa.objects.get(pk=5)
                    instance.empresas.add(empresa)
                    aprobacion_ti.eps = -1
                    aprobacion_infra.eps = -1
                    aprobacion_ti.save()
                    aprobacion_infra.save()
                if(distribucion_instance.homecare > 0):
                    empresa = Empresa.objects.get(pk=7)
                    instance.empresas.add(empresa)
                    aprobacion_ti.homecare = -1
                    aprobacion_infra.homecare = -1
                    aprobacion_ti.save()
                    aprobacion_infra.save()
                if(distribucion_instance.seguros > 0):
                    empresa = Empresa.objects.get(pk=8)
                    instance.empresas.add(empresa)
                    aprobacion_ti.seguros = -1
                    aprobacion_infra.seguros = -1
                    aprobacion_ti.save()
                    aprobacion_infra.save()
                if(distribucion_instance.solidaridad > 0):
                    empresa = Empresa.objects.get(pk=9)
                    instance.empresas.add(empresa)
                    aprobacion_ti.solidaridad = -1
                    aprobacion_infra.solidaridad = -1
                    aprobacion_ti.save()
                    aprobacion_infra.save()
                if(distribucion_instance.vida_en_plenitud > 0):
                    empresa = Empresa.objects.get(pk=10)
                    instance.empresas.add(empresa)
                    aprobacion_ti.vida_en_plenitud = -1
                    aprobacion_infra.vida_en_plenitud = -1
                    aprobacion_ti.save()
                    aprobacion_infra.save()
                if(distribucion_instance.centro_vacacional > 0):
                    empresa = Empresa.objects.get(pk=11)
                    instance.empresas.add(empresa)
                    aprobacion_ti.centro_vacacional = -1
                    aprobacion_infra.centro_vacacional = -1
                    aprobacion_ti.save()
                    aprobacion_infra.save()
                if(distribucion_instance.agencia_viajes > 0):
                    empresa = Empresa.objects.get(pk=12)
                    instance.empresas.add(empresa)
                    aprobacion_ti.agencia_viajes = -1
                    aprobacion_infra.agencia_viajes = -1
                    aprobacion_ti.save()
                    aprobacion_infra.save()
                if(distribucion_instance.gremial > 0):
                    empresa = Empresa.objects.get(pk=13)
                    instance.empresas.add(empresa)
                    aprobacion_ti.gremial = -1
                    aprobacion_infra.gremial = -1
                    aprobacion_ti.save()
                    aprobacion_infra.save()
                if(not inLineaBase(numero_solicitud)):
                	datos = getMesCra(numero_solicitud,None)
                	recursoscra = RecursosCRA(solicitud = instance, procesador = datos[7],numeroprocesadores = datos[1], memoria = datos[2], almacenamiento = datos[3])
                	recursoscra.save()


            elif 'save_temp' in request.POST :
                instance = form.save(commit=False)
                instance.user_id =  userid
                instance.estado= 'EnProcesoCoordinador'
                instance.save()
                numero_solicitud = instance.id
            # Now call the index() view.
            # The user will be shown the homepage
            messages.success(request, 'Solicitud guardada exitosamente con el numero: ')
            return render(request, 'registrosolicitud.html', {'form': form,'distribucion_form':distribucion_form,'numero_solicitud':numero_solicitud})
        else:
            # The supplied form contained errors - just print them to the terminal.
            print (form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = SolicitudForm(group = my_group)
        distribucion_form = DistribucionForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'registrosolicitud.html', {'form': form,'distribucion_form':distribucion_form})

@login_required (login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ArqSoluciones').count() == 1, login_url='/controlpanel')
def registrousuario(request):
    user = request.user
    users_in_group_arquitecto= Group.objects.get(name="ArqSoluciones").user_set.all()

    if request.method == 'POST' and user.is_authenticated() and user in users_in_group_arquitecto:
         user_form = UserForm(request.POST)
         profile_form = UserProfileForm(request.POST)

         if user_form.is_valid() and profile_form.is_valid():
            user_instance = user_form.save(commit=False)
            user_instance.set_password(user_instance.password)
            user_instance.is_staff= True
            user_instance.save()
            profile_instance = profile_form.save(commit=False)
            user_instance.groups.add(Group.objects.get(name = profile_instance.rol))
            profile_instance.user = user_instance
            profile_instance.save()
            messages.success(request, 'Usuario guardado exitosamente!')
            return render(request, 'cparqsoluciones.html', {'user_form': user_form,'profile_form': profile_form})
         else:
            # The supplied form contained errors - just print them to the terminal.
            print (user_form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'registrousuario.html', {'user_form': user_form,'profile_form': profile_form})

def modifyPerm(user):
    if user:
        if user.groups.filter(name='ArqSoluciones').count() == 1:
            print(user.groups.filter(name='ArqSoluciones').count())
            return True
        elif user.groups.filter(name='JefeInfraestructura').count() == 1:
            return True
        elif user.groups.filter(name='JefeTI').count() == 1:
            return True
        elif user.groups.filter(name='LiderInfraestructura').count() == 1:
            return True
    return False

@login_required(login_url='/')
@user_passes_test(modifyPerm, login_url='/controlpanel')
def modificarsolicitud(request):
    form_class = SolicitudForm
    my_group = str(request.user.groups.values_list('name', flat=True))
    #A HTTP POST?
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if 'search_btn' in request.POST:
            instance = form.save(commit=False)
            searchquery = instance.search_query
            try:
                query_results = Solicitud.objects.filter(id = searchquery)
                solicitud = Solicitud.objects.get(id = searchquery)
                data = {'plataforma':solicitud.plataforma,'sistemaoperativo':solicitud.sistemaoperativo,'basededatos':solicitud.basededatos,'procesador':solicitud.procesador,'procesamiento':solicitud.procesamiento,'memoria':solicitud.memoria,'almacenamiento':solicitud.almacenamiento,'backupimagenes':solicitud.backupimagenes,'estado':solicitud.estado,'tiempodeuso':solicitud.tiempodeuso,'cantidaddeusuarios':solicitud.cantidaddeusuarios,'justificacion':solicitud.justificacion}
                solicitud_form = SolicitudForm(initial=data,group = my_group)
                request.session['solicitud_encontrada']  = solicitud.id
                return render(request, "modificarsolicitud.html", {'solicitud_form':solicitud_form,'my_group':my_group,"solicitud":solicitud})
            except:
                messages.error(request, 'Solicitud no encontrada!')
                return render(request, "modificarsolicitud.html", {'form': form})

        elif 'save' in request.POST:
            if form.is_valid():
                try:
                    form = SearchForm()
                    solicitud_instance = Solicitud.objects.get(id = request.session['solicitud_encontrada'])
                    solicitud_form = SolicitudForm(request.POST, instance = solicitud_instance,group = my_group)
                    solicitud_form.save()
                    messages.success(request, 'Solicitud modificada exitosamente!')
                    return render(request, "modificarsolicitud.html", {'form': form})
                except (KeyError, Solicitud.DoesNotExist):
                    solicitud_instance = None

    else:
         # If the request was not a POST, display the form to enter details.
        form = SearchForm()
    return render(request, "modificarsolicitud.html", {'form': form})

@login_required(login_url='/')
@user_passes_test(modifyPerm, login_url='/controlpanel')

def revisarfactura(request):
    my_group = str(request.user.groups.values_list('name', flat=True))
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if 'search_btn' in request.POST:
            instance = form.save(commit=False)
            searchquery = instance.search_query

            try:
                query_results = Solicitud.objects.filter(id = searchquery)
                solicitud = Solicitud.objects.get(id = searchquery)

                data_cra = getMesCra(searchquery)

                mes_cra= data_cra[0]

                exceso_procesadores =  data_cra[1]
                exceso_memoria = data_cra[2]
                exceso_almacenamiento = data_cra[3]

                costo_exc_procesadores = data_cra[4]
                costo_exc_memoria = data_cra[5]
                costo_exc_almacenamiento = data_cra[6]

                tiempo_estimado = solicitud.tiempodeuso

                data = {'tiempodeservicio':24,'cargototal':80000,'cargoinicial':5000,'cargomeslineabase': 3260.87,'cargomescra': mes_cra,'cargomesnuevos':0 ,'id_solicitud': searchquery,'estado':'prefactura'}
                factura_form = FacturaForm(initial=data)
                id_solicitud = searchquery
                if (inLineaBase(searchquery)):
                    total_mes = 5000
                else:
                    total_mes = 5000 + mes_cra
                request.session['solicitud_encontrada']  = solicitud.id
                return render(request, "revisarfactura.html", {'my_group':my_group,'factura_form':factura_form, 'total_mes':total_mes,'id_solicitud':id_solicitud,'exceso_procesadores':exceso_procesadores,'exceso_almacenamiento':exceso_almacenamiento,'exceso_memoria':exceso_memoria,'costo_exc_procesadores':costo_exc_procesadores,'costo_exc_memoria' : costo_exc_memoria,'costo_exc_almacenamiento':costo_exc_almacenamiento,'mes_cra':mes_cra,'tiempo_estimado':tiempo_estimado})
            except:
                messages.error(request, 'La solicitud buscada no existe!')
                return render(request, "revisarfactura.html",{'form': form})
        elif 'save_bill' in request.POST:
            factura_form= FacturaForm(request.POST)
            if factura_form.is_valid():
                try:
                    data_cra = getMesCra(request.session['solicitud_encontrada'])
                    factura_form= FacturaForm(request.POST)
                    factura_instance = factura_form.save(commit=False)
                    factura_instance.id_solicitud = request.session['solicitud_encontrada']
                    solicitud_instance = Solicitud.objects.get(id = request.session['solicitud_encontrada'])
                    solicitud_instance.estado = 'EnValoracion'
                    factura_form.save()
                    numero_factura = factura_instance.id
                    messages.success(request, 'Factura guradada exitosamente, con el numero: ')
                    solicitud_instance.save()
                    return render(request, "revisarfactura.html", {'numero_factura':numero_factura,'form':form})
                except (KeyError, Solicitud.DoesNotExist):
                     print("ERROR EN EL SAVE BILL")
            elif 'aprove_bill' in request.POST:
                try:
                    data_cra = getMesCra(request.session['solicitud_encontrada'])
                    factura_form= FacturaForm(request.POST)
                    factura_instance = factura_form.save(commit=False)
                    factura_instance.id_solicitud = request.session['solicitud_encontrada']
                    solicitud_instance = Solicitud.objects.get(id = request.session['solicitud_encontrada'])
                    #if(solicitud_instance.porcentaje_de_aprobacion > 100):
                    #    solicitud_instance.estado = 'Aprobado'
                    #else:

                    factura_form.save()
                    numero_factura = factura_instance.id
                    messages.success(request, 'Factura gruadada exitosamente, con el numero: ')
                    solicitud_instance.save()
                    return render(request, "revisarfactura.html", {'numero_factura':numero_factura,'form':form})
                except (KeyError, Solicitud.DoesNotExist):
                     print("ERROR EN EL SAVE BILL")

            else:
                print(factura_form.errors)
    else:
         # If the request was not a POST, display the form to enter details.
        form = SearchForm()
    return render(request, "revisarfactura.html", {'form': form})

# def registronegociacion(request):
#     if request.method == 'POST':
#         form = NegociacionForm(request.POST)        
#         negociacion_instance = form.save(commit = False)
#         form.save()
#         return render(request,"registronegociacion.html",{'form',form})
#     else:
#          # If the request was not a POST, display the form to enter details.
#         form = NegociacionForm()
#     return render(request, "revisarfactura.html", {'form': form})
 
def inLineaBase(id_solicitud):
    print(id_solicitud)
    solicitud = Solicitud.objects.get(id = id_solicitud)
    memoria = int(re.search(r'\d+', solicitud.memoria).group())
    almacenamiento = int(re.search(r'\d+', solicitud.almacenamiento).group())
    numeroprocesadores = int (solicitud.numeroprocesadores)

    if 'Intel' in solicitud.procesador and memoria <= 64 and almacenamiento <= 300 and numeroprocesadores <= 8:
        return True
    elif 'POWER' in solicitud.procesador and memoria <= 64 and  almacenamiento <= 300 and numeroprocesadores == 1:
        return True
    else:
        return False

def getMesCra(id_solicitud,id_tiemporeal):
    solicitud = Solicitud.objects.get(id = id_solicitud)

    if not id_tiemporeal:
    	tiempodeuso = solicitud.tiempodeuso
    	diasdeuso = 0
    	horasdeuso =0
    else:
    	tiemporeal = TiempoReal.objects.get(solicitud = solicitud)
    	tiempodeuso = tiemporeal.fechafin - tiemporeal.fechainicio

    	diasdeuso = tiempodeuso.days
    	horasdeuso = tiempodeuso.seconds / 3600


    memoria = int(re.search(r'\d+', solicitud.memoria).group())
    almacenamiento = int(re.search(r'\d+', solicitud.almacenamiento).group())
    numeroprocesadores = int (solicitud.numeroprocesadores)



    #Variables de exceso
    exceso_memoria = 0
    exceso_almacenamiento = 0
    exceso_procesadores = 0

    costo_exc_memoria = 0
    costo_exc_almacenamiento = 0
    costo_exc_procesadores = 0

    subtotal_memoria = 0
    subtotal_almacenamiento = 0
    subtotal_procesadores = 0
    subtotal_dia = 0
    subtotal_mes = 0

    if 'POWER' in solicitud.procesador:
        costo_exc_memoria = float('{0:.6f}'.format(0.005))
        costo_exc_almacenamiento = float('{0:.6f}'.format(0.008))
        costo_exc_procesadores = float('{0:.6f}'.format(0.003))
        procesador = 'POWER'
        if memoria > 64:
            exceso_memoria = memoria - 64
            if almacenamiento > 300:
                exceso_almacenamiento = almacenamiento -300
                exceso_procesadores = numeroprocesadores -1
                subtotal_procesadores = exceso_procesadores * costo_exc_procesadores
                subtotal_memoria = exceso_memoria * costo_exc_memoria
                subtotal_almacenamiento = exceso_almacenamiento * costo_exc_almacenamiento
                subtotal_dia = subtotal_procesadores + subtotal_memoria +subtotal_almacenamiento
                subtotal_mes = subtotal_dia * 30
                total_cra_mes =round((subtotal_procesadores * 30) + (subtotal_memoria *30)+ (subtotal_almacenamiento * 30),2)
            else:
                total_cra_mes = round((subtotal_procesadores * 30)+ (subtotal_memoria *30),2)
        elif almacenamiento > 300:
            exceso_almacenamiento = almacenamiento -300
            exceso_procesadores = numeroprocesadores -1
            subtotal_procesadores = exceso_procesadores * costo_exc_procesadores
            subtotal_almacenamiento = exceso_almacenamiento * costo_exc_almacenamiento
            subtotal_dia = subtotal_procesadores + subtotal_almacenamiento
            subtotal_mes = subtotal_dia * 30
            total_cra_mes =round((subtotal_procesadores * 30) + (subtotal_almacenamiento * 30),2)
        else:
            total_cra_mes = round((subtotal_procesadores * 30),2)
    elif 'Intel' in solicitud.procesador:
        costo_exc_memoria = float('{0:.6f}'.format(0.006))
        costo_exc_almacenamiento =float('{0:.6f}'.format(0.008))
        costo_exc_procesadores = float('{0:.6f}'.format(0.004))
        procesador = 'Intel'
        if memoria > 64:
            exceso_memoria = memoria - 64
            if almacenamiento > 300:
                exceso_almacenamiento = almacenamiento -300
                exceso_procesadores = numeroprocesadores -1
                subtotal_procesadores = exceso_procesadores * costo_exc_procesadores
                subtotal_memoria = exceso_memoria * costo_exc_memoria
                subtotal_almacenamiento = exceso_almacenamiento * costo_exc_almacenamiento
                subtotal_dia = subtotal_procesadores + subtotal_memoria +subtotal_almacenamiento
                subtotal_mes = subtotal_dia * 30
                total_cra_mes =round((subtotal_procesadores * 30) + (subtotal_memoria * 30)+ (subtotal_almacenamiento * 30),4)
            else:
                total_cra_mes = round((subtotal_procesadores * 30)+ (subtotal_memoria  *30),4)
        elif almacenamiento > 300:
            exceso_almacenamiento = almacenamiento -300
            exceso_procesadores = numeroprocesadores -1
            subtotal_procesadores = exceso_procesadores * costo_exc_procesadores
            subtotal_memoria = exceso_memoria * costo_exc_memoria
            subtotal_almacenamiento = exceso_almacenamiento * costo_exc_almacenamiento
            subtotal_dia = subtotal_procesadores + subtotal_memoria +subtotal_almacenamiento
            subtotal_mes = subtotal_dia * 30
            total_cra_mes =round((subtotal_procesadores * 30) + (subtotal_almacenamiento * 30 ),2)
        else:
            total_cra_mes = round((subtotal_procesadores * 30),4)
    else:
        total_cra_mes = 0

    subtotal_tiempo_de_uso = subtotal_mes * int(diasdeuso)
    total_horas_uso = diasdeuso * 24 + horasdeuso
    total_cra_uso_real_almacenamiento = total_horas_uso * subtotal_almacenamiento
    total_cra_uso_real_memoria = total_horas_uso * subtotal_memoria
    total_cra_uso_real_procesadores = total_horas_uso * subtotal_procesadores
    subtotal_uso_real = total_cra_uso_real_almacenamiento + total_cra_uso_real_memoria +total_cra_uso_real_procesadores
    data = [
	    total_cra_mes,
	    exceso_procesadores,
	    exceso_memoria,
	    exceso_almacenamiento,
	    costo_exc_procesadores,
	    costo_exc_memoria,
	    costo_exc_almacenamiento,
	    procesador,
	    subtotal_almacenamiento,
	    subtotal_procesadores,
	    subtotal_memoria,
	    subtotal_dia,
	    subtotal_mes,
	    subtotal_tiempo_de_uso,
	    diasdeuso,
	    horasdeuso,
	    total_horas_uso,
	    total_cra_uso_real_almacenamiento,
	    total_cra_uso_real_memoria,
	    total_cra_uso_real_procesadores,
	    subtotal_uso_real]
    return data

def getPorcentajesCRA(id_solicitud):
	solicitud = Solicitud.objects.get(pk = id_solicitud)
	distribucion = solicitud.id_distribucion
	
	#Total de empleados por cada empresa
	
	total_financiero = int(distribucion.financiero)
	total_sugiro = int(distribucion.sugiro)
	total_vivienda = int(distribucion.vivienda)
	total_mp = int(distribucion.mp)
	total_EPS = int(distribucion.eps)
	total_EME = int(distribucion.eme)
	total_vida_en_plenitud = int(distribucion.vida_en_plenitud)
	total_centro_vacacional = int(distribucion.centro_vacacional)
	total_gremial = int(distribucion.gremial)
	total_homecare = int(distribucion.homecare)
	total_solidaridad = int(distribucion.solidaridad)
	total_agencia_viajes = int(distribucion.agencia_viajes)
	total_seguros = int(distribucion.seguros)
	
	#Cantidad de usuarios de la plataforma

	total = int(solicitud.cantidaddeusuarios)

	#Porcentaje por cada empresa

	porcentaje_financiero = round((100 * total_financiero) / total,2) 
	porcentaje_sugiro = round((100 * total_sugiro) / total,2) 
	porcentaje_vivienda = round((100 * total_vivienda) / total,2) 
	porcentaje_EME = round((100 * total_EME) / total,2) 
	porcentaje_EPS = round((100 * total_EPS) / total,2) 
	porcentaje_mp= round((100 * total_mp) / total,2) 
	porcentaje_centro_vacacional = round((100 * total_centro_vacacional) / total,2) 
	porcentaje_agencia_viajes = round((100 * total_agencia_viajes) / total,2) 
	porcentaje_homecare = round((100 * total_homecare) / total,2) 
	porcentaje_solidaridad = round((100 * total_solidaridad) / total,2) 
	porcentaje_gremial = round((100 * total_gremial) / total,2) 
	porcentaje_vida_en_plenitud = round((100 * total_vida_en_plenitud) / total,2) 
	porcentaje_seguros = round((100 * total_seguros) / total,2) 

	datos_porcentajes = [porcentaje_financiero,	porcentaje_sugiro, porcentaje_vivienda, porcentaje_mp, porcentaje_EPS, porcentaje_EME, porcentaje_homecare, porcentaje_seguros, porcentaje_solidaridad, porcentaje_vida_en_plenitud, porcentaje_centro_vacacional,porcentaje_agencia_viajes,porcentaje_gremial]

	return datos_porcentajes

def getFactura(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=somefilename.pdf'

    elements = []

    numero_solicitud = request.session['solicitud_encontrada']
    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"

    full_name = "Mike Driscoll"
    address_parts = ["411 State St.", "Marshalltown, IA 50158"]




    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))


    doc = SimpleDocTemplate(response, rightMargin=2.5*cm, leftMargin=15 * cm, topMargin=0.3 * cm, bottomMargin=0)

    data_info=[("Item","Costo (USD)"),("Cargo Total a 24 Meses",80000),("Cargo Inicial unica vez",5000),("Cargo Mes linea base 23 Meses",3260.87),("Total Parcial",8260.87)]
    table_info = Table(data_info, colWidths=(160,200), rowHeights=20)
    table_info.setStyle(TableStyle([

                       ('ALIGN',(0,0),(0,-1),'CENTER'),
                       ('VALIGN',(0,0),(0,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,0),(0,-1),colors.black),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(1,0),(1,-1),colors.black),
                        ('VALIGN',(1,0),(1,-1),'MIDDLE'),
                        ('ALIGN',(1,1),(1,-1),'RIGHT'),
                        ('ALIGN',(1,0),(1,0),'CENTER'),
                       ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),

                       ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ]))

    data_factura=[("Item","Costo"),("Costo Inicial",5000),("Costo Mes CRA",5000),("Costo Mes Nuevos",5000),("Total Mes",5000)]
    table_factura = Table(data_factura, colWidths=(160,200), rowHeights=20)
    table_factura.setStyle(TableStyle([

                       ('ALIGN',(0,0),(0,-1),'CENTER'),
                       ('VALIGN',(0,0),(0,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,0),(0,-1),colors.black),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(1,0),(1,-1),colors.black),
                        ('VALIGN',(1,0),(1,-1),'MIDDLE'),
                        ('ALIGN',(1,1),(1,-1),'RIGHT'),
                        ('ALIGN',(1,0),(1,0),'CENTER'),
                       ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),

                       ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ]))
    data_detalles=[("Item","Costo"),("Costo Inicial",5000),("Costo Mes CRA",5000),("Costo Mes Nuevos",5000),("Total Mes",5000)]
    table_detalles = Table(data_factura, colWidths=(160,200), rowHeights=20)
    table_detalles.setStyle(TableStyle([

                       ('ALIGN',(0,0),(0,-1),'CENTER'),
                       ('VALIGN',(0,0),(0,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,0),(0,-1),colors.black),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(1,0),(1,-1),colors.black),
                        ('VALIGN',(1,0),(1,-1),'MIDDLE'),
                        ('ALIGN',(1,1),(1,-1),'RIGHT'),
                        ('ALIGN',(1,0),(1,0),'CENTER'),
                       ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),

                       ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ]))



    elements.append(Spacer(10, 50))
    ptext = '<font size=12>Grupo Empresarial GES</font>'
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(10, 8))
    ptext = '<font size=12>Area de Tecnologias de la Informacion</font>'
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(10, 8))
    ptext = '<font size=12>MyCloudBillGES</font>'
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(10, 8))
    ptext = '<font size=12>ID Solicitud: %s</font>' % numero_solicitud
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(10, 50))


    ptext = '<font size=20>Factura de MyCloudBillGES</font>'
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(10, 50))
    ptext = '<font size=16>Informacion</font>'
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(1, 50))
    elements.append(table_info)
    elements.append(Spacer(1, 20))
    ptext = '<font size=16>Factura</font>'
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(1, 50))
    elements.append(table_factura)
    elements.append(Spacer(1, 20))
    ptext = '<font size=16>Detalles CRA</font>'
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(1, 50))
    elements.append(table_detalles)
    elements.append(Spacer(1, 20))
    doc.build(elements)
    return response

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}").format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('/registration/login.html', {}, context)

  # Use the login_required() decorator to ensure only those logged in can access the view.

@login_required (login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='CoordinadorSI').count() == 1, login_url='/controlpanel')
def nuevorecurso(request):
    my_group = str(request.user.groups.values_list('name', flat=True))
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if 'search_btn' in request.POST:
            instance = form.save(commit=False)
            searchquery = instance.search_query
            query_results = Solicitud.objects.filter(id = searchquery)
            try:
                solicitud = Solicitud.objects.get(id = searchquery)
                data = {'plataforma':solicitud.plataforma,'sistemaoperativo':solicitud.sistemaoperativo,'basededatos':solicitud.basededatos,'procesador':solicitud.procesador,'procesamiento':solicitud.procesamiento,'memoria':solicitud.memoria,'almacenamiento':solicitud.almacenamiento,'backupimagenes':solicitud.backupimagenes,'estado':solicitud.estado,'tiempodeuso':solicitud.tiempodeuso,'cantidaddeusuarios':solicitud.cantidaddeusuarios,'justificacion':solicitud.justificacion}
                solicitud_form = SolicitudForm(initial=data,group = my_group)
                request.session['solicitud_encontrada']  = solicitud.id
                nuevorecurso_form = NuevosRecursosForm()
                return render(request, "nuevorecurso.html", {'solicitud':solicitud,'solicitud_form':solicitud_form,'nuevorecurso_form':nuevorecurso_form})
            except:
                messages.error(request, 'La solicitud buscada no existe!')
                return render(request, "nuevorecurso.html",{'form': form})
        if 'save_rsrce' in request.POST:
            solicitud = Solicitud.objects.get(id = request.session['solicitud_encontrada'])
            periodos = calcularPeriodos(solicitud.id)
            ultimo_periodo = periodos[-1]
            ultima_fecha = ultimo_periodo.split(" - ",2)
            objeto_fecha = datetime.strptime(ultima_fecha[1],'%Y-%m-%d')
            try:
                nuevorecurso_form = NuevosRecursosForm(request.POST)
                nuevorecurso = nuevorecurso_form.save(commit=False)
                nuevorecurso.solicitud = solicitud
                nuevorecurso.fechasolicitud = datetime.now()
                if not solicitud.estado == "Aprobado":
                    if solicitud.tiempodeuso >= nuevorecurso.tiempo_de_uso:
                        nuevorecurso_form.save()
                        messages.error(request, 'Nuevo Recurso agregado con exito!')
                        return render(request, "nuevorecurso.html",{'form': form})
                    else:

                        messages.error(request, 'El tiempo de uso es mayor al de la solicitud!')
                        return render(request, "nuevorecurso.html",{'form': form})
                else:
                    if objeto_fecha > datetime.now() +  timedelta(days=int(nuevorecurso.tiempo_de_uso)*30):
                        nuevorecurso_form.save()
                        messages.error(request, 'Nuevo Recurso agregado con exito!')
                        return render(request, "nuevorecurso.html",{'form': form})

                    else:

                        messages.error(request, 'El tiempo de uso es mayor al de la solicitud!')
                        return render(request, "nuevorecurso.html",{'form': form})

            except Exception as error:
                print('caught this error: ' + repr(error))


    else:
         # If the request was not a POST, display the form to enter details.
        form = SearchForm()
    return render(request, "nuevorecurso.html", {'form': form})

@login_required (login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='LiderInfraestructura').count() == 1, login_url='/controlpanel')
def registronegociacion(request):
    if request.method == 'POST':
        negociacion_form = NegociacionForm(request.POST)
        negociacion_instance = registronegociacion_form.save(commit=False)
        negociacion_form.save()
        return render(request, "registronegociacion.html", {'negociacion_form':negociacion_form})
    else:
        negociacion_form = NegociacionForm()
    return render (request,"registronegociacion.html",{'negociacion_form':negociacion_form})

@login_required (login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='LiderInfraestructura').count() == 1, login_url='/controlpanel')
def facturaenlineabase(request):
    my_group = str(request.user.groups.values_list('name', flat=True))
    #A HTTP POST?
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if 'search_btn' in request.POST:
            instance = form.save(commit=False)
            searchquery = instance.search_query
            query_results = Solicitud.objects.filter(id = searchquery)
            solicitud = Solicitud.objects.get(id = searchquery)
            negociacion = Negociacion.objects.get(id = solicitud.negociacion.id)
            data = {'plataforma':solicitud.plataforma,'sistemaoperativo':solicitud.sistemaoperativo,'basededatos':solicitud.basededatos,'procesador':solicitud.procesador,'procesamiento':solicitud.procesamiento,'memoria':solicitud.memoria,'almacenamiento':solicitud.almacenamiento,'backupimagenes':solicitud.backupimagenes,'estado':solicitud.estado,'tiempodeuso':solicitud.tiempodeuso,'cantidaddeusuarios':solicitud.cantidaddeusuarios,'justificacion':solicitud.justificacion}
            solicitud_form = SolicitudForm(initial=data,group = my_group)
            request.session['solicitud_encontrada']  = solicitud.id
            pagos = calcularPagos(negociacion,True)
            return render(request, "facturaenlineabase.html", {'solicitud_form':solicitud_form,'negociacion':negociacion,'pagos':pagos})
        elif 'save' in request.POST:
            if form.is_valid():
                try:
                    form = SearchForm()
                    solicitud_instance = Solicitud.objects.get(id = request.session['solicitud_encontrada'])
                    solicitud_form = SolicitudForm(request.POST, instance = solicitud_instance,group = my_group)
                    solicitud_form.save()
                    messages.success(request, 'Solicitud modificada exitosamente!')
                    return render(request, "facturaenlineabase.html", {'form': form})
                except (KeyError, Solicitud.DoesNotExist):
                    solicitud_instance = None

    else:
         # If the request was not a POST, display the form to enter details.
        form = SearchForm()
    return render(request, "facturaenlineabase.html", {'form': form})

def calcularPagos(negociacion,cargoinicial):
	#Se crea una lista para dividir los pagos
	pagos=[]
	if cargoinicial == True:
		total = negociacion.cargoinicial + negociacion.cargomeslineabase
	else:
		total = negociacion.cargomeslineabase	

	financiero = round(total * 0.15 * 0.2 + total * 0.15,2)
	sugiro=round(total * 0.07 * 0.08 + total * 0.07,2)
	vivienda = round(total * 0.10 * 0.13 + total * 0.10,2)
	mp = round(total * 0.10 * 0.13 + total * 0.10,2)
	eps = round(total * 0.20 * 0.17 + total * 0.20,2)
	eme = round(total * 0.08 * 0.05 + total * 0.08,2)
	homecare = round(total * 0.04 * 0.05 + total * 0.04,2)
	seguros = round(total * 0.04 * 0.02 + total * 0.04,2)
	solidaridad = round(total * 0.05 * 0.04 + total * 0.05,2)
	vida_en_plenitud = round(total * 0.03 * 0.02 + total * 0.03,2)
	centro_vacacional = round(total * 0.03 * 0.02 + total * 0.03,2)
	agencia_viajes = round(total * 0.04 * 0.03 + total * 0.04,2)
	gremial = round(total * 0.10 * 0.11 + total * 0.10,2)
	total_pago_por_empresa = round(financiero + sugiro + vivienda + mp + eps + eme +homecare +seguros + solidaridad +vida_en_plenitud +centro_vacacional+agencia_viajes+gremial,2)
	#Se agregan los pagos a la lista

	pagos.append(financiero)
	pagos.append(sugiro)
	pagos.append(vivienda)
	pagos.append(mp)
	pagos.append(eps)
	pagos.append(eme)
	pagos.append(homecare)
	pagos.append(seguros)
	pagos.append(solidaridad)
	pagos.append(vida_en_plenitud)
	pagos.append(centro_vacacional)
	pagos.append(agencia_viajes)
	pagos.append(gremial)
	pagos.append(total_pago_por_empresa)
	return pagos

@login_required (login_url='/')
@user_passes_test(lambda u: u.groups.filter(Q(name='JefeInfraestructura') |Q(name='JefeTI')).count() == 1, login_url='/controlpanel')
def facturamensualestimada(request):
    my_group = str(request.user.groups.values_list('name', flat=True))
    #A HTTP POST?
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if 'search_btn' in request.POST:
            instance = form.save(commit=False)
            searchquery = instance.search_query
            query_results = Solicitud.objects.filter(id = searchquery)
            solicitud = Solicitud.objects.get(id = searchquery)
            data = {'plataforma':solicitud.plataforma,'sistemaoperativo':solicitud.sistemaoperativo,'basededatos':solicitud.basededatos,'procesador':solicitud.procesador,'procesamiento':solicitud.procesamiento,'memoria':solicitud.memoria,'almacenamiento':solicitud.almacenamiento,'backupimagenes':solicitud.backupimagenes,'estado':solicitud.estado,'tiempodeuso':solicitud.tiempodeuso,'cantidaddeusuarios':solicitud.cantidaddeusuarios,'justificacion':solicitud.justificacion}
            solicitud_form = SolicitudForm(initial=data,group = my_group)
            recursoscra = RecursosCRA.objects.filter(pk=searchquery)
            negociacion = Negociacion.objects.get(id = solicitud.negociacion.id)
            print ("INICIA TRY")
            try:
                tiemporeal = TiempoReal.objects.get(solicitud = solicitud)
            except Exception:
                tiemporeal = None
            print ("FIN TRY Tiempo Real")
            try:
                nuevos_recursos = NuevosRecursos.objects.filter(solicitud=solicitud)
                print(nuevos_recursos)
            except Exception:
                nuevos_recursos = None

            datos = getMesCra(searchquery,tiemporeal)
            datos_porce_cra = getPorcentajesCRA(searchquery)
            datos_cra_por_porcentaje = [
	            datos_porce_cra[0]*datos[12]*0.01,
	            datos_porce_cra[1]*datos[12]*0.01,
	            datos_porce_cra[2]*datos[12]*0.01,
	            datos_porce_cra[3]*datos[12]*0.01,
	            datos_porce_cra[4]*datos[12]*0.01,
	            datos_porce_cra[5]*datos[12]*0.01,
	            datos_porce_cra[6]*datos[12]*0.01,
	            datos_porce_cra[7]*datos[12]*0.01,
	            datos_porce_cra[8]*datos[12]*0.01,
	            datos_porce_cra[9]*datos[12]*0.01,
	            datos_porce_cra[10]*datos[12]*0.01,
	            datos_porce_cra[11]*datos[12]*0.01,
	            datos_porce_cra[12]*datos[12]*0.01,

	            datos_porce_cra[0]*datos[12]*0.01+
	            datos_porce_cra[1]*datos[12]*0.01+
	            datos_porce_cra[2]*datos[12]*0.01+
	            datos_porce_cra[3]*datos[12]*0.01+
	            datos_porce_cra[4]*datos[12]*0.01+
	            datos_porce_cra[5]*datos[12]*0.01+
	            datos_porce_cra[6]*datos[12]*0.01+
	            datos_porce_cra[7]*datos[12]*0.01+
	            datos_porce_cra[8]*datos[12]*0.01+
	            datos_porce_cra[9]*datos[12]*0.01+
	            datos_porce_cra[10]*datos[12]*0.01+
	            datos_porce_cra[11]*datos[12]*0.01+
	            datos_porce_cra[12]*datos[12]*0.01
	            ]
            pagos = calcularPagos(negociacion,False)
            total_por_empresa = [
            round(datos_cra_por_porcentaje[0] + pagos[0],2),
            datos_cra_por_porcentaje[1] + pagos[1],
            datos_cra_por_porcentaje[2] + pagos[2],
            datos_cra_por_porcentaje[3] + pagos[3],
            datos_cra_por_porcentaje[4] + pagos[4],
            datos_cra_por_porcentaje[5] + pagos[5],
            datos_cra_por_porcentaje[6] + pagos[6],
            datos_cra_por_porcentaje[7] + pagos[7],
            datos_cra_por_porcentaje[8] + pagos[8],
            datos_cra_por_porcentaje[9] + pagos[9],
            datos_cra_por_porcentaje[10] + pagos[10],
            datos_cra_por_porcentaje[11] + pagos[11],
            datos_cra_por_porcentaje[12] + pagos[12],

            round(datos_cra_por_porcentaje[0] + pagos[0]+
            datos_cra_por_porcentaje[1] + pagos[1]+
            datos_cra_por_porcentaje[2] + pagos[2]+
            datos_cra_por_porcentaje[3] + pagos[3]+
            datos_cra_por_porcentaje[4] + pagos[4]+
            datos_cra_por_porcentaje[5] + pagos[5]+
            datos_cra_por_porcentaje[6] + pagos[6]+
            datos_cra_por_porcentaje[7] + pagos[7]+
            datos_cra_por_porcentaje[8] + pagos[8]+
            datos_cra_por_porcentaje[9] + pagos[9]+
            datos_cra_por_porcentaje[10] + pagos[10]+
            datos_cra_por_porcentaje[11] + pagos[11]+
            datos_cra_por_porcentaje[12] + pagos[12],2)

            ]
            gran_total = round(total_por_empresa[0]+total_por_empresa[1]+total_por_empresa[2]+total_por_empresa[3]+total_por_empresa[4]+total_por_empresa[5]+total_por_empresa[6]+total_por_empresa[7]+total_por_empresa[8]+total_por_empresa[9]+total_por_empresa[10]+total_por_empresa[11]+total_por_empresa[12],2)

            total_cra = datos_cra_por_porcentaje[0] + datos_cra_por_porcentaje[1] + datos_cra_por_porcentaje[2]+ datos_cra_por_porcentaje[3]+ datos_cra_por_porcentaje[4]+ datos_cra_por_porcentaje[5]+ datos_cra_por_porcentaje[6]+ datos_cra_por_porcentaje[7]+ datos_cra_por_porcentaje[8]+ datos_cra_por_porcentaje[9]+ datos_cra_por_porcentaje[10]+ datos_cra_por_porcentaje[11]+ datos_cra_por_porcentaje[12]
            periodos = calcularPeriodos(searchquery)
            request.session['solicitud_encontrada']  = solicitud.id
            request.session['total_por_empresa'] = total_por_empresa

            return render(request, "facturamensualestimada.html", {'solicitud_form':solicitud_form,'recursoscra':recursoscra,'datos':datos,'datos_cra_por_porcentaje':datos_cra_por_porcentaje,'pagos':pagos,'total_por_empresa':total_por_empresa,'periodos':periodos,'negociacion':negociacion,'gran_total':gran_total,'total_cra':total_cra,"my_group":my_group,"nuevos_recursos":nuevos_recursos})
        elif 'approve_ti' in request.POST:
            if form.is_valid():
                try:
                    #form = SearchForm()
                    solicitud = Solicitud.objects.get(id = request.session['solicitud_encontrada'])
                    distribucion = solicitud.id_distribucion
                    total_distrb = getattr(distribucion,'financiero') + getattr(distribucion,'sugiro') + getattr(distribucion,'vivienda') + getattr(distribucion,'mp') + getattr(distribucion,'eps') + getattr(distribucion,'eme') + getattr(distribucion,'homecare') + getattr(distribucion,'seguros') + getattr(distribucion,'solidaridad') + getattr(distribucion,'vida_en_plenitud') + getattr(distribucion,'centro_vacacional') + getattr(distribucion,'agencia_viajes') + getattr(distribucion,'gremial')
                    #solicitud_form = SolicitudForm(request.POST, instance = solicitud_instance,group = my_group)

                    total_por_empresa = request.session['total_por_empresa']
                    user = request.user
                    perfil = UserProfile.objects.get(user=user)
                    empresa = perfil.empresa
                    nombre = empresa.nombre
                    aprobacion_ti = AprobacionTI.objects.get(solicitud=solicitud)
                    setattr(aprobacion_ti,nombre,1)
                    aprobacion_ti.save()

                    solicitud.porcentaje_de_aprobacion_ti = solicitud.porcentaje_de_aprobacion_ti + ((100 * getattr(distribucion,nombre))/total_distrb)
                    if solicitud.porcentaje_de_aprobacion_ti > 99 and solicitud.porcentaje_de_aprobacion_ti < 101:
                    	solicitud.estado = 'Aprobado'
                    solicitud.save()
                    try:
                        nuevorecurso = NuevosRecursos.objects.get(solicitud = solicitud)
                        nuevorecurso.fechasolicitud = datetime.now()
                    except NuevosRecursos.DoesNotExist:
                        messages.success(request, 'Factura aprobada exitosamente!')
                        return render(request, "facturamensualestimada.html", {'form': form,'my_group':my_group})
                    messages.success(request, 'Factura aprobada exitosamente!')
                    return render(request, "facturamensualestimada.html", {'form': form,'my_group':my_group})
                except (KeyError, Solicitud.DoesNotExist):
                    solicitud_instance = None

        elif 'approve_infra' in request.POST:
            if form.is_valid():
                try:
                    #form = SearchForm()
                    solicitud = Solicitud.objects.get(id = request.session['solicitud_encontrada'])
                    distribucion = solicitud.id_distribucion
                    total_distrb = getattr(distribucion,'financiero') + getattr(distribucion,'sugiro') + getattr(distribucion,'vivienda') + getattr(distribucion,'mp') + getattr(distribucion,'eps') + getattr(distribucion,'eme') + getattr(distribucion,'homecare') + getattr(distribucion,'seguros') + getattr(distribucion,'solidaridad') + getattr(distribucion,'vida_en_plenitud') + getattr(distribucion,'centro_vacacional') + getattr(distribucion,'agencia_viajes') + getattr(distribucion,'gremial')
                    #solicitud_form = SolicitudForm(request.POST, instance = solicitud_instance,group = my_group)

                    total_por_empresa = request.session['total_por_empresa']
                    user = request.user
                    perfil = UserProfile.objects.get(user=user)
                    empresa = perfil.empresa
                    nombre = empresa.nombre
                    aprobacion_infra = AprobacionInfra.objects.get(solicitud=solicitud)
                    setattr(aprobacion_infra,nombre,1)
                    aprobacion_infra.save()

                    solicitud.porcentaje_de_aprobacion_infra = solicitud.porcentaje_de_aprobacion_infra + ((100 * getattr(distribucion, nombre)) / total_distrb)
                    if solicitud.porcentaje_de_aprobacion_infra > 99 and solicitud.porcentaje_de_aprobacion_infra < 101:
                        solicitud.estado = 'EnValoracion'
                    solicitud.save()

                    messages.success(request, 'Factura aprobada exitosamente!')
                    return render(request, "facturamensualestimada.html", {'form': form,'my_group':my_group})
                except (KeyError, Solicitud.DoesNotExist):
                    solicitud_instance = None

    else:
         # If the request was not a POST, display the form to enter details.
        form = SearchForm()
    return render(request, "facturamensualestimada.html", {'form': form})

@login_required (login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='LiderInfraestructura').count() == 1, login_url='/controlpanel')
def facturamensualreal(request):
    my_group = str(request.user.groups.values_list('name', flat=True))
    #A HTTP POST?
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if 'search_btn' in request.POST:
            instance = form.save(commit=False)
            searchquery = instance.search_query
            query_results = Solicitud.objects.filter(id = searchquery)
            solicitud = Solicitud.objects.get(id = searchquery)
            recursoscra = RecursosCRA.objects.filter(pk=searchquery)
            negociacion = Negociacion.objects.get(id = solicitud.negociacion.id)
            tiemporeal = TiempoReal.objects.get(solicitud = solicitud)
            datos = getMesCra(searchquery,tiemporeal)
            datos_porce_cra = getPorcentajesCRA(searchquery)
            pagos = calcularPagos(negociacion,False)
            data = {'plataforma':solicitud.plataforma,'sistemaoperativo':solicitud.sistemaoperativo,'basededatos':solicitud.basededatos,'procesador':solicitud.procesador,'procesamiento':solicitud.procesamiento,'memoria':solicitud.memoria,'almacenamiento':solicitud.almacenamiento,'backupimagenes':solicitud.backupimagenes,'estado':solicitud.estado,'tiempodeuso':solicitud.tiempodeuso,'cantidaddeusuarios':solicitud.cantidaddeusuarios,'justificacion':solicitud.justificacion}
            datos_cra_por_porcentaje = [
	            round(datos_porce_cra[0]*datos[20]*0.01,2),
	            round(datos_porce_cra[1]*datos[20]*0.01,2),
	            round(datos_porce_cra[2]*datos[20]*0.01,2),
	            round(datos_porce_cra[3]*datos[20]*0.01,2),
	            round(datos_porce_cra[4]*datos[20]*0.01,2),
	            round(datos_porce_cra[5]*datos[20]*0.01,2),
	            round(datos_porce_cra[6]*datos[20]*0.01,2),
	            round(datos_porce_cra[7]*datos[20]*0.01,2),
	            round(datos_porce_cra[8]*datos[20]*0.01,2),
	            round(datos_porce_cra[9]*datos[20]*0.01,2),
	            round(datos_porce_cra[10]*datos[20]*0.01,2),
	            round(datos_porce_cra[11]*datos[20]*0.01,2),
	            round(datos_porce_cra[12]*datos[20]*0.01,2),

	            round(datos_porce_cra[0]*datos[20]*0.01+
	            datos_porce_cra[1]*datos[20]*0.01+
	            datos_porce_cra[2]*datos[20]*0.01+
	            datos_porce_cra[3]*datos[20]*0.01+
	            datos_porce_cra[4]*datos[20]*0.01+
	            datos_porce_cra[5]*datos[20]*0.01+
	            datos_porce_cra[6]*datos[20]*0.01+
	            datos_porce_cra[7]*datos[20]*0.01+
	            datos_porce_cra[8]*datos[20]*0.01+
	            datos_porce_cra[9]*datos[20]*0.01+
	            datos_porce_cra[10]*datos[20]*0.01+
	            datos_porce_cra[11]*datos[20]*0.01+
	            datos_porce_cra[12]*datos[20]*0.01,2)]
            pagos = calcularPagos(negociacion,False)
            total_por_empresa = [
            round(datos_cra_por_porcentaje[0] + pagos[0],2),
            round(datos_cra_por_porcentaje[1] + pagos[1],2),
            round(datos_cra_por_porcentaje[2] + pagos[2],2),
            round(datos_cra_por_porcentaje[3] + pagos[3],2),
            round(datos_cra_por_porcentaje[4] + pagos[4],2),
            round(datos_cra_por_porcentaje[5] + pagos[5],2),
            round(datos_cra_por_porcentaje[6] + pagos[6],2),
            round(datos_cra_por_porcentaje[7] + pagos[7],2),
            round(datos_cra_por_porcentaje[8] + pagos[8],2),
            round(datos_cra_por_porcentaje[9] + pagos[9],2),
            round(datos_cra_por_porcentaje[10] + pagos[10],2),
            round(datos_cra_por_porcentaje[11] + pagos[11],2),
            round(datos_cra_por_porcentaje[12] + pagos[12],2),

            round(datos_cra_por_porcentaje[0] + pagos[0]+
            datos_cra_por_porcentaje[1] + pagos[1]+
            datos_cra_por_porcentaje[2] + pagos[2]+
            datos_cra_por_porcentaje[3] + pagos[3]+
            datos_cra_por_porcentaje[4] + pagos[4]+
            datos_cra_por_porcentaje[5] + pagos[5]+
            datos_cra_por_porcentaje[6] + pagos[6]+
            datos_cra_por_porcentaje[7] + pagos[7]+
            datos_cra_por_porcentaje[8] + pagos[8]+
            datos_cra_por_porcentaje[9] + pagos[9]+
            datos_cra_por_porcentaje[10] + pagos[10]+
            datos_cra_por_porcentaje[11] + pagos[11]+
            datos_cra_por_porcentaje[12] + pagos[12],2)
            ]
            gran_total = total_por_empresa[0]+total_por_empresa[1]+total_por_empresa[2]+total_por_empresa[3]+total_por_empresa[4]+total_por_empresa[5]+total_por_empresa[6]+total_por_empresa[7]+total_por_empresa[8]+total_por_empresa[9]+total_por_empresa[10]+total_por_empresa[11]+total_por_empresa[12]
            total_cra = datos_cra_por_porcentaje[0] + datos_cra_por_porcentaje[1] + datos_cra_por_porcentaje[2]+ datos_cra_por_porcentaje[3]+ datos_cra_por_porcentaje[4]+ datos_cra_por_porcentaje[5]+ datos_cra_por_porcentaje[6]+ datos_cra_por_porcentaje[7]+ datos_cra_por_porcentaje[8]+ datos_cra_por_porcentaje[9]+ datos_cra_por_porcentaje[10]+ datos_cra_por_porcentaje[11]+ datos_cra_por_porcentaje[12]
            solicitud_form = SolicitudForm(initial=data,group = my_group)
            request.session['solicitud_encontrada']  = solicitud.id
            numero = 0
            try:
                	ultima_factura = Factura.objects.filter(solicitud=solicitud).latest('numero')
                	numero = ultima_factura.numero + 1
            except Factura.DoesNotExist:
            	numero = 1


                #Guardo los datos necesarios en las cookies para despues guardar la factura
            request.session['numero'] = numero
            request.session['totalporempresa'] =  total_por_empresa
            request.session['datoscraporcentaje'] =  datos_cra_por_porcentaje
            request.session['datos'] = datos

            return render(request, "facturamensualreal.html", {'solicitud_form':solicitud_form,'recursoscra':recursoscra,'negociacion':negociacion,'pagos':pagos,'datos':datos,'datos_cra_por_porcentaje':datos_cra_por_porcentaje,'total_por_empresa':total_por_empresa,'pagos':pagos,'nuevorecurso':nuevorecurso})



        elif 'aprov' in request.POST:
            try:

                solicitud = Solicitud.objects.get(id = request.session['solicitud_encontrada'])
                total_por_empresa = request.session['totalporempresa']
                numero = request.session['numero']
                datos_cra_por_porcentaje = request.session['datoscraporcentaje']
                datos = request.session['datos']

                data = {'plataforma': solicitud.plataforma, 'sistemaoperativo': solicitud.sistemaoperativo,
                        'basededatos': solicitud.basededatos, 'procesador': solicitud.procesador,
                        'procesamiento': solicitud.procesamiento, 'memoria': solicitud.memoria,
                        'almacenamiento': solicitud.almacenamiento, 'backupimagenes': solicitud.backupimagenes,
                        'estado': solicitud.estado, 'tiempodeuso': solicitud.tiempodeuso,
                        'cantidaddeusuarios': solicitud.cantidaddeusuarios, 'justificacion': solicitud.justificacion}
                solicitud_form = SolicitudForm(initial=data, group=my_group)
                recursoscra = RecursosCRA.objects.filter(pk=solicitud.id)
                negociacion = Negociacion.objects.get(id=solicitud.negociacion.id)
                tiemporeal = TiempoReal.objects.get(solicitud=solicitud)
                pagos = calcularPagos(negociacion, False)

                periodos = calcularPeriodos(solicitud.id)
                print("LOS PERIODOS SON")
                print(periodos)
                print("EL NUMERO ES")
                print(numero)
                factura = Factura.objects.create(
                    periodo=periodos[numero - 1],
                    numero=numero,
                    solicitud=solicitud,
                    financiero=total_por_empresa[0],
                    sugiro=total_por_empresa[1],
                    vivienda=total_por_empresa[2],
                    mp=total_por_empresa[3],
                    eps=total_por_empresa[4],
                    eme=total_por_empresa[5],
                    homecare=total_por_empresa[6],
                    seguros=total_por_empresa[7],
                    solidaridad=total_por_empresa[8],
                    vida_en_plenitud=total_por_empresa[9],
                    centro_vacacional=total_por_empresa[10],
                    agencia_viajes=total_por_empresa[11],
                    gremial=total_por_empresa[12])

                nuevo_recurso = NuevosRecursos.objects.filter(solicitud=solicitud)
                for item in nuevo_recurso:
                    item.fechasolicitud = datetime.now()
                    item.save()
                factura.nuevorecurso = nuevo_recurso
                factura.save()

                id_solicitud = solicitud.id
                #p = Process(target=call_command, args =("hola",))
                #p.start()
                messages.success(request, 'Factura aprobada exitosamente!')

                return render(request, "facturamensualreal.html", {'form': form})

            except (KeyError, NuevosRecursos.DoesNotExist):
                factura.save()
                return render(request, "facturamensualreal.html",
                              {'solicitud_form': solicitud_form, 'recursoscra': recursoscra, 'negociacion': negociacion,
                               'pagos': pagos, 'datos': datos, 'datos_cra_por_porcentaje': datos_cra_por_porcentaje,
                               'total_por_empresa': total_por_empresa, 'pagos': pagos})

            except (KeyError, Solicitud.DoesNotExist):
                    solicitud_instance = None


    else:
         # If the request was not a POST, display the form to enter details.
        form = SearchForm()
    return render(request, "facturamensualreal.html", {'form': form})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('')

def calcularPeriodos(id_solicitud):
    solicitud = Solicitud.objects.get(id = id_solicitud)
    #try:
    #    tiemporeal = TiempoReal.objects.get(solicitud = solicitud)
    #    tiempo_total_real = tiemporeal.fechafin - tiemporeal.fechainicio
    #    nro_meses = int(math.floor(tiempo_total_real.days / 30))
    #except TiempoReal.DoesNotExist:
    nro_meses = int(solicitud.tiempodeuso)

    fechaaprobacion = solicitud.fechaaprobacion

    fechaactual = datetime.now()
    dias=30
    periodos = []
    print("Nro de meses: "+ str(nro_meses))
    print("FECHAS: ")
    i=0
    while i != nro_meses:
        periodos.append("%s - %s" % (fechaactual, fechaactual + timedelta(days=30)))
        fechaactual = fechaactual + timedelta(days=30)
        i = i +1
    return periodos