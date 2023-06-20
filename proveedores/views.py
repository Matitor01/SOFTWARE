import json
import pandas as pd
import xlwt
#nuevas importaciones 30-05-2022
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from registration.models import Profile

from django.db.models import Count, Avg, Q
from django.shortcuts import render, redirect
from rest_framework import generics, viewsets
from rest_framework.decorators import (
	api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse, reverse_lazy
from .models import Arriendo
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from .models import Proveedor



@login_required
def proveedores_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/proveedores_main.html'
    return render(request,template_name,{'profile':profile})

@login_required
def gestion_proveedores(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/gestion_proveedores.html'
    return render(request,template_name,{'profile':profile})
##################################################################################
# proveedores crear #

@login_required
def proveedores_crear(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/proveedores_crear.html'
    return render(request,template_name,{'profile':profile})

# proveedores guardar #

@login_required
def proveedores_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')    
        rubro= request.POST.get('rubro') 
        email = request.POST.get('email') 
        telefono = request.POST.get('telefono') 
        rut = request.POST.get('rut') 

        if nombre == '' or rubro == '' or email == '' or telefono == '' or rut == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('proveedores_crear')

        proveedor = Proveedor(
            nombre=nombre,
            rubro=rubro,  
            email=email,
            telefono=telefono,
            rut=rut 
        )
        proveedor.save()
        messages.add_message(request, messages.INFO, 'proveedores ingresado con éxito')
        return redirect('proveedores_list')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')


# proveedores listar #


@login_required
def proveedores_list(request, page=None, search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    if page is None:
        page = request.GET.get('page')
    else:
        page = page

    if request.GET.get('page') is None:
        page = page
    else:
        page = request.GET.get('page')

    if search is None:
        search = request.GET.get('search')
    else:
        search = search

    if request.GET.get('search') is None:
        search = search
    else:
        search = request.GET.get('search')

    if request.method == 'POST':
        search = request.POST.get('search')
        page = None

    h_list = []
    if search is None or search == "None":
        h_count = Proveedor.objects.filter().count()
        h_list_array = Proveedor.objects.filter().order_by('nombre')
        for h in h_list_array:
            h_list.append({'id': h.id, 'nombre': h.nombre, 'rubro': h.rubro, 'email': h.email, 'telefono': h.telefono, 'rut': h.rut})
    else:
        h_count = Proveedor.objects.filter(nombre__icontains=search).count()
        h_list_array = Proveedor.objects.filter(nombre__icontains=search).order_by('nombre')
        for h in h_list_array:
            h_list.append({'id': h.id, 'nombre': h.nombre, 'rubro': h.rubro, 'email': h.email, 'telefono': h.telefono, 'rut': h.rut})

    paginator = Paginator(h_list, 20)
    h_list_paginate = paginator.get_page(page)

    template_name = 'proveedores/proveedores_list.html'
    return render(request, template_name, {'template_name': template_name, 'h_list_paginate': h_list_paginate,
                                           'paginator': paginator, 'page': page})



# proveedores ver #

@login_required
def proveedores_ver(request, proveedores_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')
    proveedores_data = Proveedor.objects.get(pk=proveedores_id)
    template_name = 'proveedores/proveedores_ver.html'
    return render (request, template_name, {'profile': profile, 'proveedores_data': proveedores_data})

# proveedores editar #

@login_required
def proveedores_edit(request, proveedores_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')

        
    
    if request.method == 'POST':
        proveedor = get_object_or_404(Proveedor, id=proveedores_id)
        nombre = request.POST.get('nombre')
        rubro = request.POST.get('rubro')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        rut = request.POST.get('rut')

        proveedor.nombre = nombre
        proveedor.rubro = rubro
        proveedor.email = email
        proveedor.telefono = telefono
        proveedor.rut = rut
        proveedor.save()

        return redirect('proveedores_ver', proveedores_id=proveedor.id)
    
    else:
        proveedor_data = Proveedor.objects.get(pk=proveedores_id)
        template_name = 'proveedores/proveedores_edit.html'
        return render(request, template_name, {'proveedor_data': proveedor_data})




# proveedores eliminar #

def proveedores_eliminar(request, proveedores_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    proveedores = get_object_or_404(Proveedor, id=proveedores_id)
    proveedores.delete()
    messages.success(request, 'cotizacion eliminada correctamente')
    return redirect('proveedores_list')
