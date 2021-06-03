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
		total = len(clientes)
		contexto = {
			'clientes':clientes,
			'total':total,
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
		idclien = int(request.POST['idclien'])
		nombre = request.POST['nombre']
		apellidopat = request.POST['apellidopat']
		apellidomat = request.POST['apellidomat']
		apodo = request.POST['apodo']
		duracion = float(request.POST['duracion'])
		idm = int(request.POST['membresia'])
		precio = 0
		with connection.cursor() as cursor:
			cursor.callproc('agregar_cliente', [idclien, nombre, apellidopat, apellidomat, apodo, duracion, idm])
			precio = cursor.fetchone()[0]
		with connection.cursor() as cursor:
			cursor.callproc('iniciar_compra')
			idcom = Compra.objects.latest('idcom').idcom
			cursor.callproc('actualizar_cliente', [idcom, idclien])
			cursor.callproc('comprar_membresia',[idcom, idclien, idm])

		if precio:
			return redirect(reverse('venta_membresia', kwargs={'pk':idcom}))

		# form = ClientesForm(request.POST)
		# if form.is_valid():
		# 	form.save()
		# 	return redirect('clientes_listar')

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
	def get(self, request, *args, **kwargs):
		cliente = Clientes.objects.get(idclien=kwargs['pk'])
		contexto = {
				'nombre':cliente.nombre,
			}
		return render(request, 'clientes_eliminar.html', contexto) 

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Confirmar':
			with connection.cursor() as cursor:
				cursor.callproc('eliminar_cliente', [kwargs['pk']])
			return redirect('clientes_listar')

		return redirect('index')

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
		elif kwargs['pk'] == 3:
			return redirect(reverse('membresias_renovar', kwargs={'pk':idclien}))


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
		return render(request, 'membresias.html', contexto)

class MembresiaRenovar(ListView):
	def get(self, request, *args, **kwargs):
		cliente = Clientes.objects.get(idclien=kwargs['pk'])
		membresias = {
			1:'Invitado',
			2:'Membresia Base',
			3:'Membresia Intermedia',
			4:'Membresia Completa',
		}

		duraciones = {
			0.25:'1 Semana',
			0.5:'2 Semanas',
			0.75:'3 Semanas',
			1:'4 Semanas',
		}

		contexto = {
			'idclien':cliente.idclien,
			'nombre':cliente.nombre,
			'apodo':cliente.apodo,
			'membresia':membresias[cliente.idmem.idmem],
			'duracion':duraciones[cliente.duracion],
		}
		return render(request, 'membresias_renovar.html', contexto)

	def post(self, request, *args, **kwargs):
		idclien = int(request.POST['idclien'])
		duracion = float(request.POST['duracion'])
		idm = int(request.POST['membresia'])

		if request.POST['confirmar'] == 'Confirmar':
			precio = 0
			with connection.cursor() as cursor:
				cursor.callproc('modificar_membresia',[idclien, idm, duracion])
				precio = cursor.fetchone()[0]

			with connection.cursor() as cursor:
				cursor.callproc('iniciar_compra')
				idcom = Compra.objects.latest('idcom').idcom
				cursor.callproc('actualizar_cliente', [idcom, idclien])
				cursor.callproc('comprar_membresia',[idcom, idclien, idm])

			if precio:
				return redirect(reverse('venta_membresia', kwargs={'pk':idcom}))
			
			
		else:
			return render(request, 'membresias')

class Producto(ListView):
	def get(self, request, *args, **kwargs):
		return render(request, 'producto_crear.html')

class ProductoFind(ListView):
	def get(self, request, *args, **kwargs):
		return render(request, 'producto_buscar.html')

	def post(self, request, *args, **kwargs):
		idprod = request.POST.get('idprod')

		try:
			producto = Productos.objects.get(idprod=idprod)
		except:
			return redirect('not_found')

		if kwargs['pk'] == 1:
			with connection.cursor() as cursor:
				cursor.callproc('buscar_bebida', [idprod])
				existe = cursor.fetchone()
			if existe:
				return redirect(reverse('producto_editar_bebida', kwargs={'pk':idprod}))

			with connection.cursor() as cursor:
				cursor.callproc('buscar_suplemento', [idprod])
				existe = cursor.fetchone()
			if existe:
				return redirect(reverse('producto_editar_suplementos', kwargs={'pk':idprod}))

			with connection.cursor() as cursor:
				cursor.callproc('buscar_ropa', [idprod])
				existe = cursor.fetchone()
			if existe:
				return redirect(reverse('producto_editar_ropa', kwargs={'pk':idprod}))
			
			return redirect(reverse('producto_editar_accesorios', kwargs={'pk':idprod}))

		elif kwargs['pk'] == 2:
			return redirect(reverse('producto_eliminar', kwargs={'pk':idprod}))
		
class ProductoEditarBebida(ListView):
	def get(self, request, *args, **kwargs):
		idprod = kwargs['pk']
		producto = Productos.objects.get(idprod=idprod)
		with connection.cursor() as cursor:
				cursor.callproc('buscar_bebida', [idprod])
				bebida = cursor.fetchone()
		contexto = {
			'idprod':idprod,
			'nombre':producto.nombreprod,
			'precio':producto.precioprod,
			'cant_mili':bebida[1],
		}

		return render(request, 'producto_editar_bebidas.html', contexto)

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Confirmar':
			idprod = request.POST['idprod']
			nombre = request.POST['nombre']
			estado_venta = int(request.POST['estado_venta'])
			cant_mili = request.POST['cant_mili']
			precio = request.POST['precio']
			with connection.cursor() as cursor:
			 	cursor.callproc('actualizar_bebida',[idprod, nombre, precio, estado_venta, cant_mili])
			return redirect('inventario_bebidas')
		return redirect('index')

class ProductoEditarSuplemento(ListView):
	def get(self, request, *args, **kwargs):
		idprod = kwargs['pk']
		producto = Productos.objects.get(idprod=idprod)
		with connection.cursor() as cursor:
				cursor.callproc('buscar_suplemento', [idprod])
				suplemento = cursor.fetchone()
		contexto = {
			'idprod':idprod,
			'nombre':producto.nombreprod,
			'precio':producto.precioprod,
			'cant_gram':suplemento[1],
		}

		return render(request, 'producto_editar_suplementos.html', contexto)

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Confirmar':
			idprod = request.POST['idprod']
			nombre = request.POST['nombre']
			estado_venta = int(request.POST['estado_venta'])
			cant_gram = request.POST['cant_gram']
			precio = request.POST['precio']
			with connection.cursor() as cursor:
			 	cursor.callproc('actualizar_suplemento',[idprod, nombre, precio, estado_venta, cant_gram])
			return redirect('inventario_suplementos')
		return redirect('index')

class ProductoEditarRopa(ListView):
	def get(self, request, *args, **kwargs):
		idprod = kwargs['pk']
		producto = Productos.objects.get(idprod=idprod)
		with connection.cursor() as cursor:
				cursor.callproc('buscar_ropa', [idprod])
				ropa = cursor.fetchone()
		contexto = {
			'idprod':idprod,
			'nombre':producto.nombreprod,
			'precio':producto.precioprod,
			'talla':ropa[2],
		}

		return render(request, 'producto_editar_ropa.html', contexto)

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Confirmar':
			idprod = request.POST['idprod']
			nombre = request.POST['nombre']
			estado_venta = int(request.POST['estado_venta'])
			talla = request.POST['talla']
			precio = request.POST['precio']
			with connection.cursor() as cursor:
			 	cursor.callproc('actualizar_ropa',[idprod, nombre, precio, estado_venta, talla])
			return redirect('inventario_ropa')
		return redirect('index')

class ProductoEditarAccesorio(ListView):
	def get(self, request, *args, **kwargs):
		idprod = kwargs['pk']
		producto = Productos.objects.get(idprod=idprod)

		contexto = {
			'idprod':idprod,
			'nombre':producto.nombreprod,
			'precio':producto.precioprod,
		}

		return render(request, 'producto_editar_accesorios.html', contexto)

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Confirmar':
			idprod = request.POST['idprod']
			nombre = request.POST['nombre']
			estado_venta = int(request.POST['estado_venta'])
			precio = request.POST['precio']
			with connection.cursor() as cursor:
			 	cursor.callproc('actualizar_accesorio',[idprod, nombre, precio, estado_venta])
			return redirect('inventario_accesorios')
		return redirect('index')

class ProductoDelete(DeleteView):
	def get(self, request, *args, **kwargs):
		producto = Productos.objects.get(idprod=kwargs['pk'])
		contexto = {
				'nombre':producto.nombreprod,
			}
		return render(request, 'producto_eliminar.html', contexto) 

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Confirmar':
			with connection.cursor() as cursor:
				cursor.callproc('eliminar_producto', [kwargs['pk']])
			return redirect('inventario')

		return redirect('index')

class SuministroBebidas(ListView):
	def get(self, request, *args, **kwargs):
		with connection.cursor() as cursor:
			cursor.callproc('iniciar_suministro')

		suministra = Suministra.objects.latest('idsum')

		try:
			idprod = Productos.objects.latest('idprod').idprod + 1
		except:
			idprod = 1

		with connection.cursor() as cursor:
			cursor.callproc('listar_proveedor')	
			proveedores = cursor.fetchall()

		contexto = {
			'idsum':suministra.idsum,
			'idprod':idprod,
			'proveedores':proveedores,
			'fecha':suministra.fechasum,
			'hora':suministra.horasum,
		}

		return render(request, 'suministro_bebidas.html', contexto)

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Registrar':
			idsum = request.POST['idsum']
			idprod = request.POST['idprod']
			idprov = request.POST['idprov']
			nombre = request.POST['nombre']
			cant = request.POST['cant']
			estado_venta = int(request.POST['estado_venta'])
			cant_mili = request.POST['cant_mili']
			precio = request.POST['precio']
			with connection.cursor() as cursor:
			 	cursor.callproc('actualizar_proveedor', [idsum, idprov])
			 	cursor.callproc('agregar_bebida',[idprod, nombre, precio, cant, estado_venta, cant_mili])
			 	cursor.callproc('suministrar_producto',[idsum, idprod, nombre, precio, cant])
			print('registrado')
			return redirect('inventario_bebidas')

		return redirect('producto_crear')

class SuministroSuplementos(ListView):
	def get(self, request, *args, **kwargs):
		with connection.cursor() as cursor:
			cursor.callproc('iniciar_suministro')

		suministra = Suministra.objects.latest('idsum')
		try:
			idprod = Productos.objects.latest('idprod').idprod + 1
		except:
			idprod = 1

		with connection.cursor() as cursor:
			cursor.callproc('listar_proveedor')	
			proveedores = cursor.fetchall()

		contexto = {
			'idsum':suministra.idsum,
			'idprod':idprod,
			'proveedores':proveedores,
			'fecha':suministra.fechasum,
			'hora':suministra.horasum,
		}

		return render(request, 'suministro_suplementos.html', contexto)

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Registrar':
			idsum = request.POST['idsum']
			idprod = request.POST['idprod']
			idprov = request.POST['idprov']
			nombre = request.POST['nombre']
			cant = request.POST['cant']
			estado_venta = int(request.POST['estado_venta'])
			cant_gram = request.POST['cant_gram']
			precio = request.POST['precio']
			with connection.cursor() as cursor:
			 	cursor.callproc('actualizar_proveedor', [idsum, idprov])
			 	cursor.callproc('agregar_suplemento',[idprod, nombre, precio, cant, estado_venta, cant_gram])
			 	cursor.callproc('suministrar_producto',[idsum, idprod, nombre, precio, cant])
			return redirect('inventario_suplementos')

		return redirect('producto_crear')

class SuministroRopa(ListView):
	def get(self, request, *args, **kwargs):
		with connection.cursor() as cursor:
			cursor.callproc('iniciar_suministro')

		suministra = Suministra.objects.latest('idsum')
		try:
			idprod = Productos.objects.latest('idprod').idprod + 1
		except:
			idprod = 1

		with connection.cursor() as cursor:
			cursor.callproc('listar_proveedor')	
			proveedores = cursor.fetchall()

		contexto = {
			'idsum':suministra.idsum,
			'idprod':idprod,
			'proveedores':proveedores,
			'fecha':suministra.fechasum,
			'hora':suministra.horasum,
		}

		return render(request, 'suministro_ropa.html', contexto)

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Registrar':
			idsum = request.POST['idsum']
			idprod = request.POST['idprod']
			idprov = request.POST['idprov']
			nombre = request.POST['nombre']
			cant = request.POST['cant']
			estado_venta = int(request.POST['estado_venta'])
			talla = request.POST['talla']
			precio = request.POST['precio']
			with connection.cursor() as cursor:
			 	cursor.callproc('actualizar_proveedor', [idsum, idprov])
			 	cursor.callproc('agregar_ropa',[idprod, nombre, precio, cant, estado_venta, talla])
			 	cursor.callproc('suministrar_producto',[idsum, idprod, nombre, precio, cant])
			return redirect('inventario_ropa')

		return redirect('producto_crear')

class SuministroAccesorios(ListView):
	def get(self, request, *args, **kwargs):
		with connection.cursor() as cursor:
			cursor.callproc('iniciar_suministro')

		suministra = Suministra.objects.latest('idsum')
		try:
			idprod = Productos.objects.latest('idprod').idprod + 1
		except:
			idprod = 1

		with connection.cursor() as cursor:
			cursor.callproc('listar_proveedor')	
			proveedores = cursor.fetchall()

		contexto = {
			'idsum':suministra.idsum,
			'idprod':idprod,
			'proveedores':proveedores,
			'fecha':suministra.fechasum,
			'hora':suministra.horasum,
		}

		return render(request, 'suministro_accesorios.html', contexto)

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Registrar':
			idsum = request.POST['idsum']
			idprod = request.POST['idprod']
			idprov = request.POST['idprov']
			nombre = request.POST['nombre']
			cant = request.POST['cant']
			estado_venta = int(request.POST['estado_venta'])
			precio = request.POST['precio']
			with connection.cursor() as cursor:
			 	cursor.callproc('actualizar_proveedor', [idsum, idprov])
			 	cursor.callproc('agregar_accesorio',[idprod, nombre, precio, cant, estado_venta])
			 	cursor.callproc('suministrar_producto',[idsum, idprod, nombre, precio, cant])
			return redirect('inventario_accesorios')

		return redirect('producto_crear')

class InventarioList(ListView):
	def get(self, request, *args, **kwargs):
		with connection.cursor() as cursor:
			cursor.callproc('inventario_general')
			inventario_general = cursor.fetchall()
		total = len(inventario_general)

		contexto = {
			'inventario_general':inventario_general,
			'total':total,
		}
		return render(request, 'inventario.html', contexto)

class InventarioAccesoriosList(ListView):
	def get(self, request, *args, **kwargs):
		with connection.cursor() as cursor:
			cursor.callproc('inventario_accesorios')
			inventario_accesorios = cursor.fetchall()

		contexto = {
			'inventario_accesorios':inventario_accesorios,
		}
		return render(request, 'inventario_accesorios.html', contexto)


class InventarioBebidasList(ListView):
	def get(self, request, *args, **kwargs):
		with connection.cursor() as cursor:
			cursor.callproc('inventario_bebidas')
			inventario_bebidas = cursor.fetchall()
		total = len(inventario_bebidas)
		contexto = {
			'inventario_bebidas':inventario_bebidas,
			'total':total,
		}
		return render(request, 'inventario_bebidas.html', contexto)

class InventarioSuplementosList(ListView):
	def get(self, request, *args, **kwargs):
		with connection.cursor() as cursor:
			cursor.callproc('inventario_suplementos')
			inventario_suplementos = cursor.fetchall()
		total = len(inventario_suplementos)

		contexto = {
			'inventario_suplementos':inventario_suplementos,
			'total':total,
		}
		return render(request, 'inventario_suplementos.html', contexto)

class InventarioRopaList(ListView):
	def get(self, request, *args, **kwargs):
		with connection.cursor() as cursor:
			cursor.callproc('inventario_ropa')
			inventario_ropa = cursor.fetchall()
		total = len(inventario_ropa)
		contexto = {
			'inventario_ropa':inventario_ropa,
			'total':total,
		}
		return render(request, 'inventario_ropa.html', contexto)

class VentaMembresia(CreateView):
	def get(self, request, *args, **kwargs):
		membresias = {
			2:'Membresia Base',
			3:'Membresia Intermedia',
			4:'Membresia Completa',
		}

		duraciones = {
			0.25:'1 Semana',
			0.5:'2 Semanas',
			0.75:'3 Semanas',
			1:'4 Semanas',
		}


		with connection.cursor() as cursor:
			cursor.callproc('buscar_compra', [kwargs['pk']])
			compra = cursor.fetchone()

		idclien = compra[1]

		with connection.cursor() as cursor:
			cursor.callproc('listar_cliente', [idclien])
			cliente = cursor.fetchone()

		contexto = {
		 	'idclien': cliente[0],
		 	'idven':compra[0],
		 	'idprod':0,
		 	'duracion':duraciones[cliente[6]],
			'idm':cliente[1],
		 	'precio':compra[4],
			'fecha':compra[2],
		 	'hora':compra[3],
		 	'membresia':membresias[cliente[1]],
		 }
		return render(request, 'ventas_crear_3.html', contexto)

	def post(self, request, *args, **kwargs):
		if request.POST['registrar'] == 'Registrar':
			return redirect('clientes_listar')
		return redirect('index')

class ProveedorCreate(CreateView):
	def get(self, request, *args, **kwargs):
		try:
			idprov = Proveedor.objects.latest('idprov').idprov + 1
		except:
			idprov = 1

		contexto = {
			'idprov':idprov,
		}
		return render(request, 'proveedor_crear.html', contexto)

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Registrar':
			idprov = request.POST.get('idprov')
			nombre = request.POST.get('nombre')
			telefono = request.POST.get('telefono')
			with connection.cursor() as cursor:
				cursor.callproc('agregar_proveedor', [idprov, nombre, telefono])
			return redirect('proveedor_listar')
		return redirect('index')

class ProveedorList(ListView):
	def get(self, request, *args, **kwargs):
		proveedores = Proveedor.objects.all()
		total = len(proveedores)
		contexto = {
			'proveedores': proveedores,
			'total':total,
		}
		return render(request, 'proveedor_listar.html', contexto)

class ProveedorUpdate(UpdateView):
	def get(self, request, *args, **kwargs):
		proveedor = Proveedor.objects.get(idprov=kwargs['pk'])
			
		contexto = {
			'idprov':proveedor.idprov,
			'nombre':proveedor.nombreprov,
			'telefono':proveedor.telefono,
		}
		return render(request, 'proveedor_editar.html', contexto)

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Editar':
			idprov = request.POST.get('idprov')
			nombre = request.POST.get('nombre')
			telefono = request.POST.get('telefono')
			with connection.cursor() as cursor:
				cursor.callproc('actualiza_proveedor', [idprov, nombre, telefono])
			return redirect('proveedor_listar')
		return redirect('index')

class ProveedorFind(ListView):
	def get(self, request, *args, **kwargs):
		return render(request, 'proveedor_buscar.html')

	def post(self, request, *args, **kwargs):
		idprov = request.POST.get('idprov')

		try:
			proveedor = Proveedor.objects.get(idprov=idprov)
		except:
			return redirect('not_found')

		if kwargs['pk'] == 1:
			return redirect(reverse('proveedor_editar', kwargs={'pk':idprov}))
		elif kwargs['pk'] == 2:
			return redirect(reverse('proveedor_eliminar', kwargs={'pk':idprov}))

class ProveedorDelete(DeleteView):
	def get(self, request, *args, **kwargs):
		proveedor = Proveedor.objects.get(idprov=kwargs['pk'])
		contexto = {
				'nombre':proveedor.nombreprov,
			}
		return render(request, 'proveedor_eliminar.html', contexto) 

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Confirmar':
			with connection.cursor() as cursor:
				cursor.callproc('elimina_proveedor', [kwargs['pk']])
			return redirect('proveedor_listar')

		return redirect('index')

class VentasCrear(CreateView):
	def get(self, request, *args, **kwargs):
		try: 
			nueva = request.POST['nueva']
		except:
			nueva = None

		if not nueva:
			with connection.cursor() as cursor:
				cursor.callproc('iniciar_compra')
				idcom = Compra.objects.latest('idcom').idcom
				cursor.callproc('buscar_compra',[idcom])
				compra = cursor.fetchone()

			contexto = {
				'idcom': idcom,
				'fecha': compra[2],
				'hora': compra[3],
				'total':compra[4],
				'nueva':'',
			}

		return render(request, 'ventas_crear.html', contexto)

	def post(self, request, *args, **kwargs):
		if request.POST['confirmar'] == 'Registrar':
			idcom = request.POST['idcom']
			idclien = request.POST['idclien']
			idprod = request.POST['idprod']
			cant = request.POST['cant']
			precio = request.POST['precio']
			with connection.cursor() as cursor:
			 	cursor.callproc('actualizar_cliente', [idcom, idclien])
			 	cursor.callproc('agregar_producto_compra',[idcom, idprod, cant])
			 	cursor.callproc('reducir_stock',[idprod, cant])
			 	cursor.callproc('buscar_compra',[idcom])
			 	compra = cursor.fetchone()

			with connection.cursor() as cursor:
				cursor.callproc('buscar_dt_compra',[idcom])
				dt_compras = cursor.fetchall()

			contexto = {
			 	'idcom': idcom,
				'fecha': compra[2],
				'hora': compra[3],
				'total':compra[4],
				'dt_compras':dt_compras,
				'nueva':'',
			 }

			return render(request, 'ventas_crear.html', contexto)

		if request.POST['confirmar'] == 'Finalizar':
			return redirect('ventas_corte')

		return redirect('index')

class VentasCorte(ListView):
	def get(self, request, *args, **kwargs):
		with connection.cursor() as cursor:
			cursor.callproc('listar_venta')
			ventas = cursor.fetchall()

		with connection.cursor() as cursor:
			cursor.callproc('total_compra_diaria')
			total = cursor.fetchone()[0]

		contexto = {
			'ventas':ventas[9:],
			'total':total,
		}
		return render(request, 'ventas_corte.html', contexto)