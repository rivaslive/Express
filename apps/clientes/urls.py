from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from apps.clientes.views import CrearPerfil,completarPerfil, membresias, detalleMembre, upgradeMem, buscarClientJSON

app_name = 'clientes'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buscarClientJSON/', buscarClientJSON, name="buscarClientJSON"),
    path('registrate/', CrearPerfil, name='sign_up'),
    path('reg_membrecia/', login_required(completarPerfil), name='reg_membrecia'),
    path('membresias/', login_required(membresias), name='membresias'),
    path('detalle_membresia/<int:pk>/', login_required(detalleMembre), name='detalle_membresia'),
    path('upgrate_mem/<int:pk>/', login_required(upgradeMem), name='upgrate_mem'),


]
