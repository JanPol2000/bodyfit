from django.db import models

class Clientes(models.Model):
    idclien = models.AutoField(db_column='idClien', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=20)
    apellidopat = models.CharField(db_column='apellidoPat', max_length=20)  # Field name made lowercase.
    apellidomat = models.CharField(db_column='apellidoMat', max_length=20)  # Field name made lowercase.
    apodo = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'clientes'

class Membresia(models.Model):
    idmem = models.AutoField(db_column='idMem', primary_key=True)  # Field name made lowercase.
    nombremem = models.CharField(db_column='nombreMem', max_length=20)  # Field name made lowercase.
    duracion = models.IntegerField()
    preciomem = models.FloatField(db_column='precioMem')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'membresia'

class Permanencia(models.Model):
    idperm = models.AutoField(db_column='idPerm', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField()

    class Meta:
        managed = False
        db_table = 'permanencia'

class PermanenciaDetallada(models.Model):
    idperm = models.ForeignKey(Permanencia, models.CASCADE, db_column='idPerm')  # Field name made lowercase.
    idclien = models.ForeignKey(Clientes, models.CASCADE, db_column='idClien')  # Field name made lowercase.
    idmem = models.ForeignKey(Membresia, models.CASCADE, db_column='idMem')  # Field name made lowercase.
    fecha = models.DateField()
    horaentrada = models.TimeField(db_column='horaEntrada')  # Field name made lowercase.
    horasalida = models.TimeField(db_column='horaSalida')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'permanencia_detallada'

class Productos(models.Model):
    idprod = models.AutoField(db_column='idProd', primary_key=True)  # Field name made lowercase.
    nombreprod = models.CharField(db_column='nombreProd', max_length=20)  # Field name made lowercase.
    stock = models.IntegerField()
    precioprod = models.FloatField(db_column='precioProd')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productos'

class Bebidas(models.Model):
    idprod = models.ForeignKey('Productos', models.CASCADE, db_column='idProd')  # Field name made lowercase.
    cantidadmililitros = models.IntegerField(db_column='cantidadMililitros')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bebidas'

class Suplementos(models.Model):
    idprod = models.ForeignKey(Productos, models.CASCADE, db_column='idProd')  # Field name made lowercase.
    cantidadgramos = models.IntegerField(db_column='cantidadGramos')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'suplementos'

class Ropa(models.Model):
    idprod = models.ForeignKey(Productos, models.CASCADE, db_column='idProd')  # Field name made lowercase.
    tipo = models.CharField(max_length=20)
    talla = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ropa'

class Compra(models.Model):
    idcom = models.AutoField(db_column='idCom', primary_key=True)  # Field name made lowercase.
    idclien = models.ForeignKey(Clientes, models.CASCADE, db_column='idClien')  # Field name made lowercase.
    fechacom = models.DateField(db_column='fechaCom')  # Field name made lowercase.
    horacom = models.TimeField(db_column='horaCom')  # Field name made lowercase.
    totalcom = models.FloatField(db_column='totalCom')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'compra'


class DetallesCompras(models.Model):
    idcom = models.ForeignKey(Compra, models.CASCADE, db_column='idCom')  # Field name made lowercase.
    idprod = models.ForeignKey('Productos', models.CASCADE, db_column='idProd')  # Field name made lowercase.
    nombreprod = models.CharField(db_column='nombreProd', max_length=20)  # Field name made lowercase.
    precioprod = models.FloatField(db_column='precioProd')  # Field name made lowercase.
    cantidadcom = models.IntegerField(db_column='cantidadCom')  # Field name made lowercase.
    subtotalcom = models.FloatField(db_column='subTotalCom')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detalles_compras'

class Proveedor(models.Model):
    idprov = models.AutoField(db_column='idProv', primary_key=True)  # Field name made lowercase.
    nombreprov = models.CharField(db_column='nombreProv', max_length=20)  # Field name made lowercase.
    telefono = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'proveedor'

class Suministra(models.Model):
    idsum = models.AutoField(db_column='idSum', primary_key=True)  # Field name made lowercase.
    idprov = models.ForeignKey(Proveedor, models.CASCADE, db_column='idProv')  # Field name made lowercase.
    fechasum = models.DateField(db_column='fechaSum')  # Field name made lowercase.
    horasum = models.TimeField(db_column='horaSum')  # Field name made lowercase.
    totalsum = models.FloatField(db_column='totalSum')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'suministra'

class DetallesSuministra(models.Model):
    idsum = models.ForeignKey('Suministra', models.CASCADE, db_column='idSum')  # Field name made lowercase.
    idprod = models.ForeignKey('Productos', models.CASCADE, db_column='idProd')  # Field name made lowercase.
    nombreprod = models.CharField(db_column='nombreProd', max_length=20)  # Field name made lowercase.
    preciosum = models.FloatField(db_column='precioSum')  # Field name made lowercase.
    cantidadsum = models.IntegerField(db_column='cantidadSum')  # Field name made lowercase.
    subtotalsum = models.FloatField(db_column='subTotalSum')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detalles_suministra'