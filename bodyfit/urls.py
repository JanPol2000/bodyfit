"""bodyfit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # Indice
    path('', Inicio.as_view(), name='index'),
    # Rutas para el CRUD del cliente
    path('clientes_listar/', ClientesList.as_view(), name='clientes_listar'),
    path('clientes_crear/', ClientesCreate.as_view(), name='clientes_crear'),
    path('clientes_buscar/<int:pk>', ClientesFind.as_view(), name='clientes_buscar'),
    path('clientes_editar/<int:pk>', ClientesUpdate.as_view(), name='clientes_editar'),
    path('clientes_eliminar/<int:pk>', ClientesDelete.as_view(), name='clientes_eliminar'),
    # Rutas para el CRUD de la membresia
    path('membresias/', MembresiaList.as_view(), name='membresias'),
    path('membresias_renovar/<int:pk>', MembresiaRenovar.as_view(), name='membresias_renovar'),
    path('inventario/', InventarioList.as_view(), name='inventario'),
    path('inventario_accesorios/', InventarioAccesoriosList.as_view(), name='inventario_accesorios'),
    path('inventario_bebidas/', InventarioBebidasList.as_view(), name='inventario_bebidas'),
    path('inventario_suplementos/', InventarioSuplementosList.as_view(), name='inventario_suplementos'),
    path('inventario_ropa/', InventarioRopaList.as_view(), name='inventario_ropa'),
    # Ruta no encontrado
    path('not_found/', not_found, name='not_found'),
    path('venta_membresia/<int:pk>', VentaMembresia.as_view(), name='venta_membresia'),
    path('producto_crear/', Producto.as_view(), name='producto_crear'),
    path('producto_buscar/<int:pk>', ProductoFind.as_view(), name='producto_buscar'),
    path('producto_eliminar/<int:pk>', ProductoDelete.as_view(), name='producto_eliminar'),
    path('producto_editar_bebida/<int:pk>', ProductoEditarBebida.as_view(), name='producto_editar_bebida'),
    path('producto_editar_suplementos/<int:pk>', ProductoEditarSuplemento.as_view(), name='producto_editar_suplementos'),
    path('producto_editar_accesorios/<int:pk>', ProductoEditarAccesorio.as_view(), name='producto_editar_accesorios'),
    path('producto_editar_ropa/<int:pk>', ProductoEditarRopa.as_view(), name='producto_editar_ropa'),
    path('suministro_bebidas/', SuministroBebidas.as_view(), name='suministro_bebidas'),
    path('suministro_suplementos/', SuministroSuplementos.as_view(), name='suministro_suplementos'),
    path('suministro_ropa/', SuministroRopa.as_view(), name='suministro_ropa'),
    path('suministro_accesorios/', SuministroAccesorios.as_view(), name='suministro_accesorios'),
    path('proveedor_crear/', ProveedorCreate.as_view(), name='proveedor_crear'),
    path('proveedor_listar/', ProveedorList.as_view(), name='proveedor_listar'),
    path('proveedor_editar/<int:pk>', ProveedorUpdate.as_view(), name='proveedor_editar'),
    path('proveedor_buscar/<int:pk>', ProveedorFind.as_view(), name='proveedor_buscar'),
    path('proveedor_eliminar/<int:pk>', ProveedorDelete.as_view(), name='proveedor_eliminar'),
    path('ventas_crear/', VentasCrear.as_view(), name='ventas_crear'),
    path('ventas_corte/', VentasCorte.as_view(), name='ventas_corte'),
]
