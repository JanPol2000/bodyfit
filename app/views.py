from django.shortcuts import render
from django.views.generic import UpdateView, DeleteView, CreateView, ListView
from .models import *
from .forms import *
from django.urls import reverse_lazy

class Inicio(ListView):
	def get(self, request, *args, **kwargs):
		return render(request, 'index.html')

# CLIENTES
# Vista para listar los clientes
class ClientesList(ListView):
	def get(self, request, *args, **kwargs):
		clientes = Clientes.objects.all()
		contexto = {
			'clientes':clientes,
		}
		return render(request, 'clientes_listar.html', contexto)

# Vista para crear los clientes
class ClientesCreate(CreateView):
	model = Clientes
	form_class = ClientesForm
	template_name = 'clientes_crear.html'
	success_url = reverse_lazy('clientes_listar')

# Vista para editar los clientes
class ClientesUpdate(UpdateView):
	model = Clientes
	form_class = ClientesForm
	template_name = 'clientes_editar.html'
	success_url = reverse_lazy('clientes_listar')

# Vista para eliminar los clientes
class ClientesDelete(DeleteView):
	model = Clientes
	template_name = 'clientes_eliminar.html'
	success_url = reverse_lazy('clientes_listar') 

# MEMBRESIA
# Vista para listar la membresia
class MembresiaList(ListView):
	def get(self, request, *args, **kwargs):
		membresias = Membresia.objects.all()
		contexto = {
			'membresias':membresias,
		}
		return render(request, 'membresia_listar.html', contexto)

# Vista para crear la membresia
class MembresiaCreate(CreateView):
	model = Membresia
	form_class = MembresiaForm
	template_name = 'membresia_crear.html'
	success_url = reverse_lazy('membresia_listar')

# Vista para editar la membresia
class MembresiaUpdate(UpdateView):
	model = Membresia
	form_class = MembresiaForm
	template_name = 'membresia_editar.html'
	success_url = reverse_lazy('membresia_listar')

# Vista para eliminar la membresia
class MembresiaDelete(DeleteView):
	model = Membresia
	template_name = 'membresia_eliminar.html'
	success_url = reverse_lazy('membresia_listar')

# PROVEEDOR
# Vista para crear a proveedor
class ProveedorList(ListView):
	def get(self, request, *args, **kwargs):
		proveedores = Proveedor.objects.all()
		contexto = {
			'proveedores':proveedores,
		}
		return render(request, 'proveedor_listar.html', contexto)

# Vista para crear al proveedor
class ProveedorCreate(CreateView):
	model = Proveedor
	form_class = ProveedorForm
	template_name = 'proveedor_crear.html'
	success_url = reverse_lazy('proveedor_listar')

# Vista para editar al proveedor
class ProveedorUpdate(UpdateView):
	model = Proveedor
	form_class = ProveedorForm
	template_name = 'proveedor_editar.html'
	success_url = reverse_lazy('proveedor_listar')

# Vista para eliminar la proveedor
class ProveedorDelete(DeleteView):
	model = Proveedor
	template_name = 'proveedor_eliminar.html'
	success_url = reverse_lazy('proveedor_listar')

# PRODUCTOS
# Vista para crear el producto
class ProductosList(ListView):
	def get(self, request, *args, **kwargs):
		productos = Productos.objects.all()
		contexto = {
			'productos':productos,
		}
		return render(request, 'productos_listar.html', contexto)
# Vista para crear el producto
class ProductosCreate(CreateView):
	model = Productos
	form_class = ProductosForm
	template_name = 'productos_crear.html'
	success_url = reverse_lazy('productos_listar')

# Vista para editar el producto
class ProductosUpdate(UpdateView):
	model = Productos
	form_class = ProductosForm
	template_name = 'productos_editar.html'
	success_url = reverse_lazy('productos_listar')

# Vista para eliminar el producto
class ProductosDelete(DeleteView):
	model = Productos
	template_name = 'productos_eliminar.html'
	success_url = reverse_lazy('productos_listar')


