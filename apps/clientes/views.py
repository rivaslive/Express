import json

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Q

from apps.clientes.forms import ClienteForm, MembresiaForm
# Create your views here.
from apps.clientes.models import Cliente, Membresia, TipoMembresia, Operacion


def CrearPerfil(request):
    if request.method == 'POST':
        usernames = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password1', '')
        if password == password2:
            # Create user and save to the database
            user = User.objects.create_user(usernames, '', password)
            # Update fields and then save again
            user.save()
            return redirect('login')
        else:
            return render(request, 'base/error404.html')
    else:
        return render(request, 'registration/perfil_form.html')


def completarPerfil(request):
    tipoMembrecia = request.POST.get('tipoM', '')
    print("SU metodo ES: " + str(request.POST))
    if request.method == "POST":
        form = ClienteForm(request.POST)
        print("SU FORM ES: " + str(form))
        if form.is_valid():
            post = form.save()
            form2 = MembresiaForm({'cliente': post.pk, 'tipoMembresia': tipoMembrecia})
            if form2.is_valid():
                form2.save()
                messages.success(request, 'Membresia Exitosa')
                return redirect('clientes:mostrar_clientes')
            else:
                messages.success(request, 'Se creó el cliente')
            return redirect('clientes:mostrar_clientes')

        else:
            messages.warning(request, "Informacion Incorrecta 1")
            return redirect('clientes:membresias')

    else:
        form = ClienteForm
        membresias = TipoMembresia.objects.all().exclude(estado=0)
        return render(request, 'clientes/crearMembresias.html', {'form': form, 'tipoMembrecia': membresias})


def membresias(request):
    query = Membresia.objects.all().order_by('-estado')
    return render(request, 'clientes/membresias.html', {'clientes': query})


def detalleMembre(request, pk):
    membresia = Membresia.objects.get(pk=pk)
    operation = Operacion.objects.filter(Membresia=pk)
    return render(request, 'clientes/detalle_membresia.html', {'member': membresia, 'operations': operation})

def upgradeMem(request, pk):
    tipoMem = request.POST.get('tipo', '')
    if request.method == 'POST':
        form = get_object_or_404(Membresia, pk=pk)
        tipoMem = int(tipoMem)
        print(str(form.tipoMembresia_id))
        if tipoMem == form.tipoMembresia_id:
            msg = "Seleccione una membresia distinta a la que tiene"
            messages.warning(request, msg)
        else:
            form.tipoMembresia_id = tipoMem
            form.save()
            msg = "Membrecia actualizada con exito"
            messages.success(request, msg)
        return redirect('clientes:membresias')

    else:
        tipo = TipoMembresia.objects.all().exclude(estado=0)
        return render(request, 'clientes/upgradeMembre.html', {'tipo': tipo, 'pk':pk})


@csrf_exempt
def buscarClientJSON(request):
    buscar = request.POST.get('valor', '')
    print("EL VALOR ES: " + str(buscar))
    queryset = Membresia.objects.values('pk', 'cliente__nombre').filter(cliente__nombre=buscar)
    query = list()

    for entry in queryset[::-1]:
        query.append(entry)

    print(query)
    data = {'membresias': query}
    data = json.dumps(data)

    #print(str(data))
    return JsonResponse(data, safe=False)

def mostrarClientes(request):
    clientes = Cliente.objects.all().exclude(estado=0)
    return render(request, 'clientes/clientes_dashboard.html',{'clientes': clientes})

def mostrarClientesDes(request):
    clientes = Cliente.objects.all().exclude(estado=1)
    return render(request, 'clientes/clientesDeshabilitados.html',{'clientes': clientes})



def editarCliente(request, pk):
    clientes = Cliente.objects.get(pk=pk)
    if request.method == 'GET':
        form = ClienteForm(instance=clientes)
    else:
        form = ClienteForm(request.POST, instance=clientes)
        if  form.is_valid():
            form.save()
            messages.success(request,'Cliente editado correctamente')
            return redirect('clientes:mostrar_clientes')
        messages.warning(request,'Error al editar el cliente')
        return redirect('clientes:mostrar_clientes')
    return render(request,'clientes/crearMembresias.html',{'form':form, 'pk':pk,'clientes':clientes})

def deshabilitarCliente(request,pk):
    clientes = Cliente.objects.get(pk=pk)
    if request.method == "POST":
        respuesta = get_object_or_404(Cliente,pk=clientes.pk)
        respuesta.estado = 0
        respuesta.save()
        messages.success(request, 'Cliente deshabilitado')
        return  redirect('clientes:mostrar_clientes')
    return render(request,'clientes/cambiarEstadoCliente.html',{'clientes':clientes,'pk':pk})

def habilitarCliente(request,pk):
    clientes = Cliente.objects.get(pk=pk)
    if request.method == "POST":
        respuesta = get_object_or_404(Cliente, pk=clientes.pk)
        respuesta.estado = 1
        respuesta.save()
        messages.success(request, 'Cliente habilitado')
        return redirect('clientes:mostrar_clientes')
    return render(request, 'clientes/cambiarEstadoCliente.html', {'clientes': clientes, 'pka': pk})

def buscarClienteActivo(request):
    busqueda = request.GET.get('search','')
    query = Cliente.objects.filter(Q(nombre__contains=busqueda ) | Q(marca__contains=busqueda)).exclude(estado=0).order_by('nombre')
    print(query)
    return render(request, 'clientes/clientes_dashboard.html',{'clientes':busqueda, 'query':query})




