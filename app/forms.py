from django import forms
from .models import *

class ClientesForm(forms.ModelForm):
	class Meta:
		model = Clientes 
		fields = '__all__'

class MembresiaForm(forms.ModelForm):
	class Meta:
		model = Membresia 
		fields = '__all__'

class ProveedorForm(forms.ModelForm):
	class Meta:
		model = Proveedor 
		fields = '__all__'

class ProductosForm(forms.ModelForm):
	class Meta:
		model = Productos 
		fields = '__all__'