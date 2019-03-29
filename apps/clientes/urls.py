from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from apps.clientes.views import CrearPerfil,completarPerfil,\
    membresias, detalleMembre, upgradeMem, buscarClientJSON, \
    mostrarClientes, editarCliente, deshabilitarCliente, mostrarClientesDes, habilitarCliente, buscarClienteActivo

app_name = 'clientes'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buscarClientJSON/', buscarClientJSON, name="buscarClientJSON"),
    path('buscarCliente/', buscarClienteActivo, name="buscarClienteActivo"),
    path('registrate/', CrearPerfil, name='sign_up'),
    path('reg_membrecia/', login_required(completarPerfil), name='reg_membrecia'),
    path('membresias/', login_required(membresias), name='membresias'),
    path('mostrar_clientes/', login_required(mostrarClientes), name='mostrar_clientes'),
    path('mostrar_clientesDes/', login_required(mostrarClientesDes), name='mostrar_clientes_des'),
    path('detalle_membresia/<int:pk>/', login_required(detalleMembre), name='detalle_membresia'),
    path('deshabilitarCliente/<int:pk>/', login_required(deshabilitarCliente), name='deshabilitarCliente'),
    path('habilitarCliente/<int:pk>/', login_required(habilitarCliente), name='habilitarCliente'),
    path('editar_cliente/<int:pk>/', login_required(editarCliente), name='editar_cliente'),
    path('upgrate_mem/<int:pk>/', login_required(upgradeMem), name='upgrate_mem'),


]
