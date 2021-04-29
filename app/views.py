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