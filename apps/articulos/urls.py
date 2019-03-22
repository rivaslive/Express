from django.urls import path, re_path
from apps.articulos.views import articulo, inventario_response, habilitarArticulo,mostrarDeshabilitados,inventario, \
    CrearArticulo, articuloDetalle, buscar, inicio, generador, articulo_edi, actualizarEstado, buscarJSON#ArticuloListClass, articuloListJSON,
from django.contrib.auth.decorators import login_required
#from  rest_framework.urlpatterns import format_suffix_patterns
from apps.ventas.views import graficas

app_name='articulo'

urlpatterns = [
    path('generador/', login_required(generador) , name="generador"),
    path('buscar/', login_required(buscar) , name="buscar"),
    path('buscar_json/', login_required(buscarJSON) , name="buscar_json"),
    path('index/', login_required(inicio), name="index"),
    path('articulo/', login_required(articulo), name="articulo"),
    path('articulo_detalle/<int:pk>/', login_required(articuloDetalle), name="articuloDetalle"),
    path('editarInventario/<int:pk>/', login_required(articulo_edi), name="editarInventario"),
    path('darBaja/<int:pk>/', login_required(actualizarEstado), name="darBaja"),
    path('darAlta/<int:pk>/', login_required(habilitarArticulo), name="darAlta"),

    path('crearArticulo/', login_required(CrearArticulo.as_view()), name="crearArticulo"),
    path('inventario/', login_required(inventario), name="inventario"),
    path('inventario_response/', login_required(inventario_response), name="inventario_response"),
    path('deshabilitado/', login_required(mostrarDeshabilitados), name="deshabilitado"),
    #path('articulo_list_json/', articuloListJSON, name="articulo_list_json"),
    #path('articulo_list/', ArticuloListClass.as_view(), name="articuloList"),


]

#urlpatterns = format_suffix_patterns(urlpatterns)