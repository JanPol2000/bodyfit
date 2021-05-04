from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView, CreateView, ListView
from .models import *
from .forms import *
from django.urls import reverse_lazy, reverse 
from django.db import connection
 
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
	def get(self, request, *args, **kwargs):
		try:
			idclien = Clientes.objects.latest('idclien').idclien
			idclien += 1
		except:
			idclien = 1

		contexto = {
			'idclien':idclien,
		}
		return render(request, 'clientes_crear.html', contexto)

	def post(self, request, *args, **kwargs):
		form = ClientesForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('clientes_listar')
		return render(request, 'clientes_crear.html')

# Vista para editar los clientes
class ClientesUpdate(UpdateView):
	def get(self, request, *args, **kwargs):
		cliente = Clientes.objects.filter(idclien=kwargs['pk'])

		contexto = {
			'cliente': cliente[0],
		}
		return render(request, 'clientes_editar.html', contexto)

	def post(self, request, *args, **kwargs):
		cliente = Clientes.objects.get(idclien=kwargs['pk'])
		form = ClientesForm(request.POST, instance=cliente)
		if form.is_valid():
			form.save()
			return redirect('clientes_listar')
		return render(request, 'clientes_crear.html')

# Vista para eliminar los clientes
class ClientesDelete(DeleteView):
	model = Clientes
	template_name = 'clientes_eliminar.html'
	success_url = reverse_lazy('clientes_listar') 

#Vista para buscar a los clientes
class ClientesFind(ListView):
	def get(self, request, *args, **kwargs):
		return render(request, 'clientes_buscar.html')

	def post(self, request, *args, **kwargs):
		idclien = request.POST.get('idclien')
		try:
			cliente = Clientes.objects.get(idclien=idclien)
		except:
			return redirect('not_found')

		if kwargs['pk'] == 1:
			return redirect(reverse('clientes_editar', kwargs={'pk':idclien}))
		elif kwargs['pk'] == 2:
			return redirect(reverse('clientes_eliminar', kwargs={'pk':idclien}))

def not_found(request):
	return render(request, 'not_found.html')
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


