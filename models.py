# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bebidas(models.Model):
    idprod = models.ForeignKey('Productos', models.DO_NOTHING, db_column='idProd')  # Field name made lowercase.
    cantidadmililitros = models.IntegerField(db_column='cantidadMililitros')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bebidas'


class Clientes(models.Model):
    idclien = models.AutoField(db_column='idClien', primary_key=True)  # Field name made lowercase.
    idmem = models.ForeignKey('Membresia', models.DO_NOTHING, db_column='idMem')  # Field name made lowercase.
    nombre = models.CharField(max_length=20)
    apellidopat = models.CharField(db_column='apellidoPat', max_length=20)  # Field name made lowercase.
    apellidomat = models.CharField(db_column='apellidoMat', max_length=20)  # Field name made lowercase.
    apodo = models.CharField(max_length=20)
    duracion = models.FloatField()

    class Meta:
        managed = False
        db_table = 'clientes'


class Compra(models.Model):
    idcom = models.AutoField(db_column='idCom', primary_key=True)  # Field name made lowercase.
    idclien = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='idClien')  # Field name made lowercase.
    fechacom = models.DateField(db_column='fechaCom')  # Field name made lowercase.
    horacom = models.TimeField(db_column='horaCom')  # Field name made lowercase.
    totalcom = models.FloatField(db_column='totalCom')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'compra'


class DetallesCompras(models.Model):
    idcom = models.ForeignKey(Compra, models.DO_NOTHING, db_column='idCom')  # Field name made lowercase.
    idprod = models.ForeignKey('Productos', models.DO_NOTHING, db_column='idProd')  # Field name made lowercase.
    nombreprod = models.CharField(db_column='nombreProd', max_length=50)  # Field name made lowercase.
    precioprod = models.FloatField(db_column='precioProd')  # Field name made lowercase.
    cantidadcom = models.IntegerField(db_column='cantidadCom')  # Field name made lowercase.
    subtotalcom = models.FloatField(db_column='subTotalCom')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detalles_compras'


class DetallesSuministra(models.Model):
    idsum = models.ForeignKey('Suministra', models.DO_NOTHING, db_column='idSum')  # Field name made lowercase.
    idprod = models.ForeignKey('Productos', models.DO_NOTHING, db_column='idProd')  # Field name made lowercase.
    nombreprod = models.CharField(db_column='nombreProd', max_length=20)  # Field name made lowercase.
    preciosum = models.FloatField(db_column='precioSum')  # Field name made lowercase.
    cantidadsum = models.IntegerField(db_column='cantidadSum')  # Field name made lowercase.
    subtotalsum = models.FloatField(db_column='subTotalSum')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detalles_suministra'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Membresia(models.Model):
    idmem = models.AutoField(db_column='idMem', primary_key=True)  # Field name made lowercase.
    nombremem = models.CharField(db_column='nombreMem', max_length=50)  # Field name made lowercase.
    duracion = models.CharField(max_length=15)
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
    idperm = models.ForeignKey(Permanencia, models.DO_NOTHING, db_column='idPerm')  # Field name made lowercase.
    idclien = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='idClien')  # Field name made lowercase.
    fecha = models.DateField()
    horaentrada = models.TimeField(db_column='horaEntrada')  # Field name made lowercase.
    horasalida = models.TimeField(db_column='horaSalida')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'permanencia_detallada'


class Productos(models.Model):
    idprod = models.AutoField(db_column='idProd', primary_key=True)  # Field name made lowercase.
    nombreprod = models.CharField(db_column='nombreProd', max_length=50)  # Field name made lowercase.
    stock = models.IntegerField()
    precioprod = models.FloatField(db_column='precioProd')  # Field name made lowercase.
    estado_venta = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productos'


class Proveedor(models.Model):
    idprov = models.AutoField(db_column='idProv', primary_key=True)  # Field name made lowercase.
    nombreprov = models.CharField(db_column='nombreProv', max_length=50)  # Field name made lowercase.
    telefono = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'proveedor'


class Ropa(models.Model):
    idprod = models.ForeignKey(Productos, models.DO_NOTHING, db_column='idProd')  # Field name made lowercase.
    tipo = models.CharField(max_length=20)
    talla = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ropa'


class Suministra(models.Model):
    idsum = models.AutoField(db_column='idSum', primary_key=True)  # Field name made lowercase.
    idprov = models.ForeignKey(Proveedor, models.DO_NOTHING, db_column='idProv')  # Field name made lowercase.
    fechasum = models.DateField(db_column='fechaSum')  # Field name made lowercase.
    horasum = models.TimeField(db_column='horaSum')  # Field name made lowercase.
    totalsum = models.FloatField(db_column='totalSum')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'suministra'


class Suplementos(models.Model):
    idprod = models.ForeignKey(Productos, models.DO_NOTHING, db_column='idProd')  # Field name made lowercase.
    cantidadgramos = models.IntegerField(db_column='cantidadGramos')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'suplementos'
