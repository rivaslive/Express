import json
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
#from rest_framework import status, generics

from apps.articulos.models import Articulo, Categoria
from apps.articulos.forms import ArticuloForm
from django.db.models import Sum, Q
import random
#from rest_framework.decorators import api_view
#from rest_framework.response import Response
#from apps.articulos.serializers import ArticuloSerializer

# ver articulos
from apps.ventas.models import detalle
import json
# from chartjs.views.lines import BaseLineChartView
from django.views.generic import TemplateView


def articulo(request):
    try:
        if request.session['codigo']:
            request.session['codigo'] = ''
            print ("CODIGO ADMIN RESETEADO")
    except:
        request.session['codigo'] = ''
        print ("CODIGO ADMIN RESETEADO")

    query = Articulo.objects.filter(is_activate=1).order_by('-pk')

    return render(request, 'articulos/articulo.html', {'articulo': query})


# ver articulos


def articuloDetalle(request, pk):
    query = Articulo.objects.get(id=pk)
    return render(request, 'articulos/articuloDetalle.html', {'articulo': query})


# crear articulos
class CrearArticulo(SuccessMessageMixin, CreateView):
    template_name = 'articulos/productoModal.html'
    form_class = ArticuloForm

    def get_success_url(self):
        return reverse_lazy('articulo:articulo')

    success_message = 'Operacion Exitosa'


def inventario_response(request):
    # Articulos con estado activo, con stock mayor que 1 pero menores que 10
    query = Articulo.objects.filter(Q(stock__gt=0) & Q(stock__lt=11)).exclude(is_activate=0).order_by('stock')
    # Articulos con 0 existencias
    query_ar = Articulo.objects.filter(stock=0).exclude(is_activate=0).order_by('stock')

    query_are = Articulo.objects.filter(stock__gt=10).exclude(is_activate=0).order_by('stock')
    #print("CODIGO SESSION: " + request.session['codigo'])
    return render(request, 'articulos/inventario.html',
                  {'inventario1': query, 'inventario': query_ar, 'inventariop': query_are, 'correcto':'1'})


# Mostrar los articulos sin stock
def inventario(request):
    codigo = request.POST.get('codigo', '')
    try:
        if codigo:
            request.session['codigo'] = codigo
            codigoSession = codigo
            #print ("EL CODIGO ES: " + codigoSession)
        else:
            codigoSession = request.session['codigo']
    except:
        codigoSession = '0'
    if codigoSession == "adminroot" or codigo == "adminroot":
        return inventario_response(request)
    else:
        request.session['codigo'] = ''
        if codigo:
            messages.warning(request, 'Codigo Incorrecto')
            return redirect('articulo:articulo')
        return render(request, 'base/codigo.html')

    # Buscar Articulos


def buscar(request):
    try:
        if request.session['codigo']:
            request.session['codigo'] = ''
            print ("CODIGO ADMIN RESETEADO")
    except:
        request.session['codigo'] = ''
        print ("CODIGO ADMIN RESETEADO")
    buscar = request.GET.get('search', '')
    queryset = Articulo.objects.filter(Q(nombre_articulo__icontains=buscar) | Q(codigo_articulo__contains=buscar) | Q(id_categoria__nombre_Categoria__contains=buscar)).exclude(is_activate=0).order_by(
        'nombre_articulo')

    return render(request, 'articulos/articulo.html', {'articulo': queryset, 'busqueda': buscar})

@csrf_exempt
def buscarJSON(request):
    buscar = request.POST.get('valor', '')
    print("EL VALOR ES: " + str(buscar))
    queryset = Articulo.objects.values('codigo_articulo','nombre_articulo','stock').filter(
        Q(nombre_articulo__icontains=buscar) | Q(codigo_articulo__contains=buscar) | Q(id_categoria__nombre_Categoria__contains=buscar)).exclude(is_activate=0).order_by(
        'nombre_articulo')
    query = list()

    for entry in queryset[::-1]:
        query.append(entry)
    data = {'articulos':query}
    data = json.dumps(data)

    #print(str(data))
    return JsonResponse(data, safe=False)

def inicio(request):
    try:
        if request.session['codigo']:
            request.session['codigo'] = ''
            print ("CODIGO ADMIN RESETEADO")
    except:
        request.session['codigo'] = ''
        print ("CODIGO ADMIN RESETEADO")
    dataset = detalle.objects.values('id_articulo__nombre_articulo').exclude(id_venta__estado=1).annotate(
        total=Sum('cantidad')).order_by('-sub_total')[:5]
    print(dataset)
    categories = list()
    survived_series_data = list()

    for entry in dataset[::-1]:
        categories.append('%s ' % entry['id_articulo__nombre_articulo'])
        gananc = entry['total']
        totali = round(gananc, 2)
        survived_series_data.append(totali)

    survived_series = {
        'name': 'Productos',
        'data': survived_series_data,
        "colorByPoint": True,
    }
    chart = {
        'chart': {'type': 'column'},
        'title': {'text': '5 articulos mas vendidos'},
        'xAxis': {'categories': categories},
        'yAxis': {'title': {'text': 'Cantidades en Unidades'}},
        'series': [survived_series]
    }
    dump = json.dumps(chart)

    dataset2 = detalle.objects.values('id_articulo__nombre_articulo').exclude(id_venta__estado=1).annotate(
        total=Sum('cantidad')).order_by('sub_total')[:5]
    print(dataset2)
    categories = list()
    survived_series_data = list()
    datos = list()
    for entry in dataset2[::-1]:
        categories.append('%s ' % entry['id_articulo__nombre_articulo'])
        gananc = entry['total']
        totali = round(gananc, 2)
        survived_series_data.append(totali)
    i = 0
    for s in survived_series_data:
        datos.append({'name': categories[i], 'y': s})
        i = i + 1

    survived_series = {
        'name': 'Articulos',
        'data': datos,
        "colorByPoint": 'true',
    }
    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': '5 articulos menos vendidos'},
        'series': [survived_series]
    }
    print(chart)
    dump2 = json.dumps(chart)

    fechaNOW = datetime.now()
    return render(request, 'base/inicio.html', {'charte': dump, 'charte2': dump2, 'fecha': fechaNOW})


def generador(request):
    try:
        if request.session['codigo']:
            request.session['codigo'] = ''
            print ("CODIGO ADMIN RESETEADO")
    except:
        request.session['codigo'] = ''
        print ("CODIGO ADMIN RESETEADO")
    try:
        evaluation = request.POST.get('evaluation', '')
        if evaluation:
            articulos = Articulo.objects.values_list('codigo_articulo', flat=True).order_by('pk')
            print(articulos)
            i = 0
            while i == 0:
                codigo = random.randrange(1000000, 99999999, 1)
                articulos = Articulo.objects.filter(codigo_articulo=codigo).count()
                print(articulos)
                if articulos == 0:
                    return render(request, 'articulos/generador.html', {'codigo': codigo})
                else:
                    print("funciona")
        else:
            return render(request, 'articulos/generador.html')
    except:
        return render(request, 'articulos/generador.html')


def articulo_edi(request, pk):
    articulo = Articulo.objects.get(id=pk)
    cat = Categoria.objects.all()
    if request.method == 'GET':
        form = ArticuloForm(instance=articulo)
    else:
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Articulo editado correctamente')
            return redirect('articulo:articulo')
        messages.warning(request, 'error al editar articulo')
        return redirect('articulo:articulo')
    return render(request, 'articulos/productoModal.html',{'form': form, 'pk': pk, 'articulo': articulo, 'categorias': cat})


def actualizarEstado(request, pk):
    arti = Articulo.objects.get(id=pk)
    if request.method == 'POST':
        respuesta = get_object_or_404(Articulo, pk=arti.pk)
        respuesta.is_activate = 0
        respuesta.save()
        messages.success(request, 'Articulo deshabilitado')
        return redirect('articulo:articulo')
    return render(request, 'articulos/cambiarEstadoModal.html', {'arti': arti, 'pk': pk})


def mostrarDeshabilitados(request):
    try:
        if request.session['codigo']:
            request.session['codigo'] = ''
            print ("CODIGO ADMIN RESETEADO")
    except:
        request.session['codigo'] = ''
        print ("CODIGO ADMIN RESETEADO")
    query = Articulo.objects.filter(is_activate=0).order_by('id')
    return render(request, 'articulos/articuloDeshabilitado.html', {'inventario': query})


def habilitarArticulo(request, pk):
    arti = Articulo.objects.get(id=pk)
    if request.method == 'POST':
        respuesta = get_object_or_404(Articulo, pk=arti.pk)
        respuesta.is_activate = 1
        respuesta.save()
        messages.success(request, 'Articulo Habilitado')
        return redirect('articulo:articulo')
    return render(request, 'articulos/cambiarEstadoModal.html', {'articulo': arti, 'pka': pk})


"""@api_view(['GET', 'POST'])
def articuloListJSON(request, format=None):
    if request.method == 'GET':
        articulos = Articulo.objects.all()
        serializer = ArticuloSerializer(articulos, many=True)
        datos = json.dumps(serializer.data)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ArticuloSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticuloListClass(generics.ListCreateAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer"""
