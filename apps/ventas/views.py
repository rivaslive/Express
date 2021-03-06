import json
from datetime import datetime, timedelta

from django.contrib import messages
from django.db.models import Q, Sum
from django.shortcuts import render, redirect, get_object_or_404, render_to_response

# Create your views here.

from apps.articulos.models import Articulo
from apps.clientes.forms import OperacionForm
from apps.clientes.models import Membresia

from apps.ventas.forms import VentaForm, DetalleForm, FacturaForm
from apps.ventas.models import detalle, Venta, Factura


def prueba(request):
    return render(request, 'base/admin.html')



def shop(request):
    try:
        if request.session['codigo']:
            request.session['codigo'] = ''
            print ("CODIGO ADMIN RESETEADO")
    except:
        request.session['codigo'] = ''
        print ("CODIGO ADMIN RESETEADO")
    try:
        ventaId = request.session['ventaId']
        if ventaId:
            query = detalle.objects.filter(id_venta=ventaId)
            if query:
                total = 0
                for foo in query:
                    total += foo.sub_total
            else:
                total = 0
            print('ventaId 0', query)
            return render(request, 'ventas/shop.html', {'query': query, 'total': total})
        else:
            request.session['ventaId'] = ""
            return render(request, 'ventas/shop.html')
    except:
        request.session['ventaId'] = ""
        return render(request, 'ventas/shop.html')


def venta(request):
    descuento = request.POST.get('desc', '')
    cantidad = request.POST.get('cantidad', '')
    codigo = request.POST.get('codigo', '')
    cliente = request.POST.get('cliente2', '')
    try:
        articulo = Articulo.objects.get(codigo_articulo=codigo)
    except:
        messages.warning(request, '01 No existe el codigo de registro: ' + request.GET.get('codigo', ''))
        return redirect('ventas:shop')

    if request.session['ventaId'] == '':
        dateNow = datetime.now()
        print(dateNow)
        print("PRESENTACION EN UNIDADES")
        if cantidad:
            if int(cantidad) <= articulo.stock:
                print("INTENTANDO APLICAR DESC DE: " + str(descuento))
                form = VentaForm({'fecha_venta': dateNow, 'cliente':cliente,'estado': 1})
                if form.is_valid():
                    obtener = form.save(commit=False)
                    obtener.save()
                    print('SU ID DE VENTA ES ', obtener.pk)
                    request.session['ventaId'] = obtener.pk
                    if descuento:
                        if float(descuento) <= 100:
                            # descuento sin porcentaje
                            descuento2 = float(float(descuento) / 100)
                            print("SU DESC ES: " + str(descuento2))
                            # valor del precio total
                            valor = float(int(cantidad) * articulo.precio_unidad)
                            # descuento al total el descuento
                            subTotal = float("{0:.2f}".format(valor - (valor * descuento2)))
                            descuentoValor = float("{0:.2f}".format(valor * descuento2))
                            print('EL SUBTOTAL ES: ' + str(subTotal))
                        else:
                            messages.warning(request, "ingrese un descuento menor del 100%")
                            return redirect('ventas:shop')

                    else:
                        valor = 0
                        subTotal = float(int(cantidad) * articulo.precio_unidad)
                        descuentoValor = 0
                        print('EL SUBTOTAL ES: ' + str(subTotal))
                    form2 = DetalleForm(
                        {'cantidad': cantidad, 'precio': articulo.precio_unidad, 'descuento': descuentoValor,
                         'sub_total': subTotal,
                         'descuentoPorcentual': descuento,
                         'id_articulo': articulo.pk,
                         'id_venta': request.session['ventaId']})
                    if form2.is_valid():
                        form2.save()
                        form3 = get_object_or_404(Articulo, pk=articulo.pk)
                        form3.stock = (articulo.stock - int(cantidad))
                        form3.save()

                        messages.success(request, 'Operacion Exitosa')
                        return redirect('ventas:venta')

                    else:
                        messages.warning(request, 'Error en registro detalle')
                        return redirect('ventas:shop')
                else:
                    messages.warning(request, 'Error en registro')
                    return redirect('ventas:shop')
            else:
                messages.warning(request, 'No hay suficientes existencias')
                return redirect('ventas:shop')
        else:
            messages.warning(request, 'Ingrese una cantidad')
            return redirect('ventas:shop')
    else:
        print('VENTA EXISTENTE ID NUMERO ', request.session['ventaId'])
        if cantidad:
            if int(cantidad) <= articulo.stock:
                ventaId = request.session['ventaId']
                try:
                    existens = detalle.objects.filter(Q(id_venta=ventaId) & Q(id_articulo__codigo_articulo=codigo))
                    if existens:
                        evaluador = 1
                        print('estamos aqui 3')
                    else:
                        evaluador = 0
                    print("Evaluador: " + str(evaluador))
                except:
                    evaluador = 0
                if evaluador == 0:
                    print("VENTA ACTIVA Y NO ARTICULO SIN COINCIDIR")
                    if descuento:
                        if float(descuento) <= 100:
                            descuento2 = float(float(descuento) / 100)
                            print("SU DESC ES: " + str(descuento2))
                            valor = float(int(cantidad) * articulo.precio_unidad)
                            subTotal = float("{0:.2f}".format(valor - (valor * descuento2)))
                            print('EL SUBTOTAL ES: ' + str(subTotal))
                            descuentoValor = float("{0:.2f}".format(valor * descuento2))
                        else:
                            messages.warning(request, "ingrese un descuento menor del 100%")
                            return redirect('ventas:shop')
                    else:
                        valor = 0
                        subTotal = float(int(cantidad) * articulo.precio_unidad)
                        print('EL SUBTOTAL ES: ' + str(subTotal))
                        descuentoValor = 0
                    form2 = DetalleForm(
                        {
                            'cantidad': cantidad,
                            'precio': articulo.precio_unidad,
                            'descuento': descuentoValor,
                            'sub_total': subTotal,
                            'descuentoPorcentual': descuento,
                            'id_articulo': articulo.pk,
                            'id_venta': ventaId
                        }
                    )
                    if form2.is_valid():
                        form2.save()
                        # Editar el registro ya existe de articulo para restar el stock
                        form3 = get_object_or_404(Articulo, pk=articulo.pk)
                        form3.stock = (articulo.stock - int(cantidad))
                        form3.save()
                        messages.success(request, 'Operacion Exitosa')
                        return redirect('ventas:venta')
                    else:
                        messages.warning(request, 'Formulario no valido')
                        return redirect('ventas:shop')
                else:
                    print('ARTICULO YA EXISTENTE EN LA VENTA')
                    if descuento:
                        if float(descuento) <= 100:
                            descuento2 = float(float(descuento) / 100)
                            print("SU DESC ES: " + str(descuento2))
                            valor = float(int(cantidad) * articulo.precio_unidad)
                            subTotal = float("{0:.2f}".format(valor - (valor * descuento2)))
                            print('EL SUBTOTAL ES: ' + str(subTotal))
                            descuentoValor = float("{0:.2f}".format(valor * descuento2))

                        else:
                            messages.warning(request, "ingrese un descuento menor del 100%")
                            return redirect('ventas:shop')

                    else:
                        valor = 0
                        subTotal = float(int(cantidad) * articulo.precio_unidad)
                        print('EL SUBTOTAL ES: ' + str(subTotal))
                        descuentoValor = 0
                    detal = detalle.objects.get(Q(id_venta=ventaId) & Q(id_articulo__codigo_articulo=codigo))
                    print(detal.pk)
                    print("DETALLE VENTA NUMERO: " + str(detal.pk))
                    post = get_object_or_404(detalle, pk=detal.pk)
                    post.cantidad = (detal.cantidad + int(cantidad))
                    post.descuento = float(float(detal.descuento) + descuentoValor)
                    post.descuentoPorcentual = descuento
                    post.sub_total = (float(detal.sub_total) + subTotal)
                    post.save()
                    # Editar el registro ya existe de articulo para restar el stock
                    form3 = get_object_or_404(Articulo, pk=articulo.pk)
                    form3.stock = (articulo.stock - int(cantidad))
                    form3.save()
                    messages.success(request, 'Operacion Exitosa')
                    return redirect('ventas:venta')
            else:
                messages.warning(request, 'No hay suficientes existencias')
                return redirect('ventas:shop')
        else:
            messages.warning(request, 'Ingrese una Cantidad')
            return redirect('ventas:shop')


def eliminarDetalle(request, pk):
    detalles = detalle.objects.get(id=pk)
    pk2 = detalles.id_articulo.pk
    cantidad = detalles.cantidad
    if detalles:
        detalles.delete()
        articulos = Articulo.objects.get(id=pk2)
        if articulos:
            form3 = get_object_or_404(Articulo, pk=pk2)
            form3.stock += cantidad
            form3.save()
            messages.success(request, 'Registro Eliminado correctamente, se agrego ' + str(
                cantidad) + " Unid a " + articulos.nombre_articulo)
            return redirect('ventas:shop')
        else:
            messages.warning(request, 'Error al sumar el STOCK')
            return redirect('ventas:shop')
    else:
        messages.warning(request, 'Error al eliminar detalle')
        return redirect('ventas:shop')


def vender(request):
    try:
        if request.session['codigo']:
            request.session['codigo'] = ''
            print ("CODIGO ADMIN RESETEADO")
    except:
        request.session['codigo'] = ''
        print ("CODIGO ADMIN RESETEADO")
    ventaId = request.session['ventaId']
    if ventaId != "":
        if request.method == "POST":
            try:
                facturas = Factura.objects.latest('id')
            except:
                print("estamos en 1")
                facturas = ""
            if facturas != "":
                print("estamos en 2")
                detalles = detalle.objects.filter(id_venta=ventaId)
                if detalles:
                    total = 0
                    descuentoTotal = 0
                    for foo in detalles:
                        total += foo.sub_total
                        descuentoTotal += foo.descuento
                else:
                    total = 0
                    descuentoTotal = 0
                efectivo = float(request.POST.get('cambio', ''))
                if efectivo >= float(total):
                    print("estamos en 3")
                    cambio = float("{0:.2f}".format(efectivo - float(total)))
                    numero = (facturas.numero + 1)
                    ventas = Venta.objects.get(id=ventaId)
                    print(ventas)
                    form = FacturaForm({'venta': ventaId, 'total': total, 'cambio': cambio, 'fecha': ventas.fecha_venta,
                                        'numero': numero, 'efectivo': float(efectivo), 'descuentoTotal':descuentoTotal})
                    print(form)
                    print("paso error")
                    if form.is_valid():
                        print("estamos en 4")
                        form.save()
                        print("estamos en 4")
                        if ventas:
                            print("estamos en 5")
                            form = get_object_or_404(Venta, pk=ventas.pk)
                            form.estado = 0
                            form.save()
                            messages.success(request, "Venta exitosa")
                            return redirect('ventas:ticket')
                        else:
                            messages.warning(request, "No se pudo finalizar la venta")
                            return redirect('ventas:shop')
                    else:
                        messages.warning(request, "No se pudo crear el Ticket")
                        return redirect('ventas:shop')
                else:
                    messages.warning(request, "Ingrese un monto MAYOR al total")
                    return redirect('ventas:shop')
            else:
                print("estamos en 6")
                efectivo = float(request.POST.get('cambio', ''))
                detalles = detalle.objects.filter(id_venta=ventaId)
                if detalles:
                    total = 0
                    descuentoTotal = 0
                    for foo in detalles:
                        total += foo.sub_total
                        descuentoTotal += foo.descuento
                else:
                    total = 0
                    descuentoTotal = 0
                if efectivo >= float(total):
                    print("estamos en 7")
                    cambio = float("{0:.2f}".format(efectivo - float(total)))
                    print(cambio)
                    numero = 1
                    ventas = Venta.objects.get(id=ventaId)
                    form = FacturaForm(
                        {'venta': ventaId, 'total': total, 'cambio': float(cambio), 'fecha': ventas.fecha_venta,
                         'numero': numero, 'efectivo': efectivo, 'descuentoTotal': descuentoTotal})
                    if form.is_valid():
                        print("estamos en 8")
                        form.save()
                        if ventas:
                            print("estamos en 9")
                            form = get_object_or_404(Venta, pk=ventas.pk)
                            form.estado = 0
                            form.save()
                            print("exito")
                            messages.success(request, "Operacion exitosa")
                            return redirect('ventas:ticket')
                        else:
                            messages.warning(request, "No se pudo finalizar la venta")
                            return redirect('ventas:shop')
                    else:
                        print('error')
                        messages.warning(request, "No se pudo crear el Ticket")
                        return redirect('ventas:shop')
                else:
                    messages.warning(request, "Ingrese un monto MAYOR al total")
                    return redirect('ventas:shop')
        else:
            messages.warning(request, "error metodo POST")
            return redirect('ventas:shop')
    else:
        messages.warning(request, "No existe ninguna venta activa")
        return redirect('ventas:shop')


def ticket(request):
    try:
        if request.session['codigo']:
            request.session['codigo'] = ''
            print ("CODIGO ADMIN RESETEADO")
    except:
        request.session['codigo'] = ''
        print ("CODIGO ADMIN RESETEADO")
    ventaId = request.session['ventaId']
    try:
        facturas = Factura.objects.get(venta_id=ventaId)
        print(facturas)
        detalles = detalle.objects.filter(id_venta=ventaId)
        request.session['ventaId'] = ""
        return render(request, 'ventas/ticket.html', {'detalle': detalles, 'factura': facturas})
    except:
        return render(request, 'ventas/ticket.html')


# Elimina la venta actual
def drop(request):
    ventaId = request.session['ventaId']

    if ventaId:
        try:
            venta = Venta.objects.get(id=ventaId)
            detalles = detalle.objects.filter(id_venta=ventaId)

        except:
            messages.warning(request, "error en ID de venta")
            return redirect('ventas:shop')

        for d in detalles:
            idArt = d.id_articulo.pk
            cantidad = d.cantidad
            form = get_object_or_404(Articulo, pk=idArt)
            form.stock += cantidad
            form.save()
            d.delete()
            print("Paso TODO")
        if venta:
            venta.delete()
            request.session['ventaId'] = ""
            messages.success(request, "Venta eliminada con exito")
            return redirect('ventas:shop')
        else:
            messages.warning(request, "error en eliminar venta")
            return redirect('ventas:shop')
    else:
        messages.warning(request, "no existe ninguna venta")
        return redirect('ventas:shop')


def editarShop(request, pk):
    try:
        if request.session['codigo']:
            request.session['codigo'] = ''
            print ("CODIGO ADMIN RESETEADO")
    except:
        request.session['codigo'] = ''
        print ("CODIGO ADMIN RESETEADO")
    detalles = detalle.objects.get(id=pk)

    if request.method == "GET":
        desc = ''
        form = detalles
    else:
        descuento = request.POST.get('desc', '')
        cantidad = request.POST.get('cantidad', '')
        codigo = request.POST.get('codigo', '')
        articulo = Articulo.objects.get(codigo_articulo=codigo)
        if articulo.stock == 0:
            if int(cantidad) <= detalles.cantidad:
                try:
                    form = get_object_or_404(Articulo, pk=articulo.pk)
                    form.stock = articulo.stock + (detalles.cantidad - int(cantidad))
                    form.save()
                    try:
                        print("ESTO ES 1")
                        if descuento:
                            if float(descuento) <= 100:
                                # descuento sin porcentaje
                                descuento2 = float(float(descuento) / 100)
                                print("SU DESC ES: " + str(descuento2))
                                # valor del precio total
                                valor = float(int(cantidad) * detalles.id_articulo.precio_unidad)
                                # descuento al total el descuento
                                subTotal = float("{0:.2f}".format(valor - (valor * descuento2)))
                                descuentoValor = float("{0:.2f}".format(valor * descuento2))
                                print('EL SUBTOTAL ES: ' + str(subTotal))
                            else:
                                messages.warning(request, "ingrese un descuento menor del 100%")
                                return redirect('ventas:shop')
                        else:
                            descuento=0
                            subTotal = float(int(cantidad) * detalles.id_articulo.precio_unidad)
                            descuentoValor = 0
                            print('EL SUBTOTAL ES: ' + str(subTotal))

                        form = get_object_or_404(detalle, pk=pk)
                        form.cantidad = int(cantidad)
                        form.descuento = float(descuentoValor)
                        form.descuentoPorcentual = float(descuento)
                        form.sub_total = subTotal
                        form.save()
                        messages.success(request, "Operacion exitosa se sumaron " + str(cantidad) + " al stock")
                        return redirect('ventas:shop')
                    except:
                        messages.warning(request, "error al cargar nueva cantidad")
                        return redirect('ventas:shop')
                except:
                    messages.warning(request, "error al cargar stock")
                    return redirect('ventas:shop')
            else:
                messages.warning(request, "error stock insuficiente")
                return redirect('ventas:shop')
        else:
            if int(cantidad) == detalles.cantidad:
                try:
                    print("ESTO ES 2")
                    try:
                        form = get_object_or_404(Articulo, pk=articulo.pk)
                        form.stock = articulo.stock + (detalles.cantidad - int(cantidad))
                        form.save()
                    except:
                        messages.warning(request, "error al cargar stock")
                        return redirect('ventas:shop')
                    if descuento:

                        if float(descuento) <= 100:
                            # descuento sin porcentaje
                            descuento2 = float(float(descuento) / 100)
                            print("SU DESC ES: " + str(descuento2))
                            # valor del precio total
                            valor = float(int(cantidad) * detalles.id_articulo.precio_unidad)
                            # descuento al total el descuento
                            subTotal = float("{0:.2f}".format(valor - (valor * descuento2)))
                            descuentoValor = float("{0:.2f}".format(valor * descuento2))
                            print('EL SUBTOTAL ES: ' + str(subTotal))
                        else:
                            messages.warning(request, "ingrese un descuento menor del 100%")
                            return redirect('ventas:shop')
                    else:
                        descuento = 0
                        subTotal = float(int(cantidad) * detalles.id_articulo.precio_unidad)
                        descuentoValor = 0
                        print('EL SUBTOTAL ES: ' + str(subTotal))
                    form = get_object_or_404(detalle, pk=detalles.pk)
                    form.cantidad = int(cantidad)
                    form.descuento = float(descuentoValor)
                    form.sub_total = subTotal
                    form.descuentoPorcentual = float(descuento)
                    form.save()
                    messages.success(request, "Operacion exitosa se sumaron " + str(cantidad) + " al stock")
                    return redirect('ventas:shop')
                except:
                    messages.warning(request, "error al cargar nueva cantidad")
                    return redirect('ventas:shop')

            else:
                if (int(cantidad) - detalles.cantidad) <= articulo.stock :
                    try:
                        print("ESTO ES 1")
                        try:
                            form = get_object_or_404(Articulo, pk=articulo.pk)
                            form.stock = articulo.stock + (detalles.cantidad - int(cantidad))
                            form.save()
                        except:
                            messages.warning(request, "error al cargar stock")
                            return redirect('ventas:shop')
                        if descuento:
                            if float(descuento) <= 100:
                                # descuento sin porcentaje
                                descuento2 = float(float(descuento) / 100)
                                print("SU DESC ES: " + str(descuento2))
                                # valor del precio total
                                valor = float(int(cantidad) * detalles.id_articulo.precio_unidad)
                                # descuento al total el descuento
                                subTotal = float("{0:.2f}".format(valor - (valor * descuento2)))
                                descuentoValor = float("{0:.2f}".format(valor * descuento2))
                                print('EL SUBTOTAL ES: ' + str(subTotal))
                            else:
                                messages.warning(request, "ingrese un descuento menor del 100%")
                                return redirect('ventas:shop')
                        else:
                            descuento = 0
                            subTotal = float(int(cantidad) * detalles.id_articulo.precio_unidad)
                            descuentoValor = 0
                            print('EL SUBTOTAL ES: ' + str(subTotal))
                        form = get_object_or_404(detalle, pk=detalles.pk)
                        form.cantidad = int(cantidad)
                        form.descuento = float(descuentoValor)
                        form.descuentoPorcentual = float(descuento)
                        form.sub_total = subTotal
                        form.save()
                        messages.success(request, "Operacion exitosa se sumaron " + str(cantidad) + " al stock")
                        return redirect('ventas:shop')
                    except:
                        messages.warning(request, "error al cargar nueva cantidad")
                        return redirect('ventas:shop')
                else:
                    messages.warning(request, "No hay suficiente stock")
                    return redirect('ventas:shop')
    ventaId = request.session['ventaId']
    if ventaId:
        query = detalle.objects.filter(id_venta=ventaId)
        if query:
            total = 0
            for foo in query:
                total += (foo.cantidad * foo.id_articulo.precio_unidad)
        else:
            total = 0
        print('ventaId 0', query)

        return render(request, 'ventas/shop.html', {'form': form, 'query': query, 'total': total, 'desc': desc})
    else:
        request.session['ventaId'] = ""
        return render(request, 'ventas/shop.html', {'form': form, 'desc': desc})


def listarVentas(request):
    return render(request, 'ventas/listVentas.html')


def llenarTablaVentas(request):

    codigo = request.POST.get('codigo', '')
    try:
        if codigo:
            request.session['codigo'] = codigo
            codigoSession = codigo
            #print ("EL CODIGO ES: "+codigoSession)
        else:
            codigoSession = request.session['codigo']
    except:
        codigoSession = '0'
    if codigoSession == "adminroot" or codigo == "adminroot":

        query = Venta.objects.all().exclude(estado=1).order_by('-fecha_venta')
        return render(request, 'ventas/listVentas.html', {'datosVenta': query, 'correcto':'1'})
    else:
        if codigo:
            messages.warning(request, 'Codigo Incorrecto')
            return redirect('articulo:articulo')
        return render(request, 'base/codigo.html', {'listVenta': 1})


def detalleVenta(request, pk):
    total = 0
    ventaDetalle = detalle.objects.filter(id_venta=pk)
    for sumaTotal in ventaDetalle:
        total += sumaTotal.sub_total
    return render(request, 'ventas/detalleVenta.html', {'detalleVenta': ventaDetalle, 'pk': pk, "total": total})


def regresarVentas(request, pk):
    vntas = Venta.objects.get(id=pk)
    print(vntas)
    if vntas:
        res = get_object_or_404(Venta, pk=vntas.pk)
        res.estado = 1
        res.save()
        request.session['ventaId'] = pk
        messages.success(request, 'Venta Recuperada')
        return redirect('ventas:shop')
    return render(request, 'ventas/listVentas.html', {'pkV': pk, 'ventas': vntas})

def reporte(request):
    try:
        if request.session['codigo']:
            request.session['codigo'] = ''
            print ("CODIGO ADMIN RESETEADO")
    except:
        request.session['codigo'] = ''
        print ("CODIGO ADMIN RESETEADO")
    fechaNow =  datetime.now()
    print (fechaNow)
    query = detalle.objects.filter(id_venta__fecha_venta=fechaNow).exclude(id_venta__estado=1)
    total = 0
    total2 = 0
    for q in query:
        total += q.sub_total

    fechaAfter = fechaNow - timedelta(days=30)
    query2 = detalle.objects.filter(id_venta__fecha_venta__gte=fechaAfter).exclude(id_venta__estado=1)
    for q in query2:
        total2 += q.sub_total
    query3 = Articulo.objects.all().exclude(is_activate=0)

    return render(request, 'ventas/arqueo.html', {'query':query,'query2':query2,'query3':query3, 'total':total, 'fecha':fechaNow,'total2':total2, 'fecha2':fechaAfter})


def graficas(request):
    try:
        if request.session['codigo']:
            request.session['codigo'] = ''
            print ("CODIGO ADMIN RESETEADO")
    except:
        request.session['codigo'] = ''
        print ("CODIGO ADMIN RESETEADO")
    dataset = detalle.objects.values('id_articulo__nombre_articulo').exclude(id_venta__estado=1).annotate(
        total=Sum('cantidad')).order_by('-sub_total')[:5]
    print (dataset)
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
    print (dataset2)
    categories = list()
    survived_series_data = list()
    datos = list()
    for entry in dataset2[::-1]:
        categories.append('%s ' % entry['id_articulo__nombre_articulo'])
        gananc = entry['total']
        totali = round(gananc, 2)
        survived_series_data.append(totali)
    i=0
    for s in survived_series_data:
        datos.append({'name':categories[i], 'y':s})
        i= i+1

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
    return render(request, 'articulos/index.html',
                  {'charte': dump, 'charte2': dump2, 'fecha': fechaNOW})






def venderServicios(request):
    data = request.POST
    if request.method == "POST":
        membresia = data.get('Membrecia', '')
        operacion = data.get('tipoOperacion', '')
        descuento = 0
        observaciones = data.get('observaciones', '')
        if membresia == 1:
            descuento = 0.05
        form = OperacionForm({})
    else:
        membresias = Membresia.objects.all().exclude(estado=0)
        return render_to_response('ventas/servicios.html', {'membresias':membresias})

