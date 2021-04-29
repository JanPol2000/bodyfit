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
]
