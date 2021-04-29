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
    path('clientes_editar/<int:pk>', ClientesUpdate.as_view(), name='clientes_editar'),
    path('clientes_eliminar/<int:pk>', ClientesDelete.as_view(), name='clientes_eliminar'),
    # Rutas para el CRUD de la membresia
    path('membresia_listar/', MembresiaList.as_view(), name='membresia_listar'),
    path('membresia_crear/', MembresiaCreate.as_view(), name='membresia_crear'),
    path('membresia_editar/<int:pk>', MembresiaUpdate.as_view(), name='membresia_editar'),
    path('membresia_eliminar/<int:pk>', MembresiaDelete.as_view(), name='membresia_eliminar'),
    # Rutas para el CRUD del proveedor
    path('proveedor_listar/', ProveedorList.as_view(), name='proveedor_listar'),
    path('proveedor_crear/', ProveedorCreate.as_view(), name='proveedor_crear'),
    path('proveedor_editar/<int:pk>', ProveedorUpdate.as_view(), name='proveedor_editar'),
    path('proveedor_eliminar/<int:pk>', ProveedorDelete.as_view(), name='proveedor_eliminar'),
]
