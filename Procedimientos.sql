# Procedimientos
# Ejemplo
# delimiter $$
# create procedure mostrarProductos()
# begin
# 	select * from productos;
# end$$
# delimiter ;

# Iniciar compra
DELIMITER $$ #
CREATE PROCEDURE iniciar_compra ()
BEGIN
	INSERT INTO compra (idClien, fechaCom, horaCom, totalCom) VALUES (1, curdate(), curtime(), 0); # Creamos una nueva compra, con un total igual a 0
END$$
DELIMITER ;

DELIMITER $$ #
CREATE PROCEDURE actualizar_cliente (idcompra INT, idc INT)
BEGIN
	UPDATE compra SET idClien = idc WHERE idcom = idcompra;
END$$
DELIMITER ;

# Agregar producto
DELIMITER $$
CREATE PROCEDURE agregar_producto_compra (idCompra INT, idProducto INT, cantidad INT)
BEGIN
	set @nombre = (select nombreProd from productos where idProd=idProducto); # Guardamos el nombre del producto en una variable
	set @precio = (select precioProd from productos where idProd=idProducto); # Guardamos el precio del producto en una variable
	set @sub = @precio*cantidad; # Guardamos el subtotal de lo que lleva el cliente
	insert into detalles_compras (idCom, idProd, nombreProd, precioProd, cantidadCom, subTotalCom) values (idCompra, idProducto, @nombre, @precio, cantidad, @sub); # Agregamos un nuevo producto a la lista de compra
	set @total = (select sum(subTotalCom) from detalles_compras where idCom = idCompra); # Calculamos el total de la compra
    update compra set totalCom = @total where idCom = idCompra; # Actualizamos la informacion
END$$
DELIMITER ;



# Reducir stock
DELIMITER $$
CREATE PROCEDURE reducir_stock (idProducto INT, cantidad INT)
BEGIN
	UPDATE productos SET stock = stock-cantidad WHERE idProd = idProducto; # Disminuimos el stock dependiendo de la cantidad comprada
END$$
DELIMITER ;

# Buscar compra
DELIMITER $$ #
CREATE PROCEDURE buscar_compra (id INT)
BEGIN
	SELECT * FROM compra WHERE idCom = id; # Busca una compra en especifico
END$$
DELIMITER ;

# Buscar detalle compra
DELIMITER $$
CREATE PROCEDURE buscar_dt_compra (id INT)
BEGIN
	SELECT * FROM detalles_compras WHERE idCom = id; # Busca los productos comprados detalladamente de una compra general
END$$
DELIMITER ;

# Buscar producto
DELIMITER $$
CREATE PROCEDURE buscarProd (id INT)
BEGIN
	SELECT * FROM productos WHERE idProd = id; # Buscamos un preducto en especifico
END$$
DELIMITER ;

# Agregar cliente
DELIMITER $$ #
CREATE PROCEDURE agregar_cliente (idC INT, nombreC VARCHAR (20), apellidoP VARCHAR (20), apellidoM VARCHAR (20), apodo VARCHAR (15), duracion FLOAT, idM INT)
BEGIN
	INSERT INTO clientes VALUES (idC, idM, nombreC, apellidoP, apellidoM, apodo, duracion);
	set @costo = duracion * (SELECT precioMem FROM membresia WHERE idMem = idM);
    select @costo;
END$$
DELIMITER ;

# Inventario general
DELIMITER $$ #
CREATE PROCEDURE inventario_general ()
BEGIN
	SELECT * FROM productos;
END$$
DELIMITER ;

# Inventario bebidas
DELIMITER $$ #
CREATE PROCEDURE inventario_bebidas ()
BEGIN
	SELECT productos.idProd, nombreProd, stock, precioProd, cantidadMililitros FROM productos RIGHT OUTER JOIN bebidas on bebidas.idProd = productos.idProd;
END$$
DELIMITER ;

# Inventario suplemento
DELIMITER $$ #
CREATE PROCEDURE inventario_suplementos ()
BEGIN
	SELECT productos.idProd, nombreProd, stock, precioProd, cantidadGramos FROM productos RIGHT OUTER JOIN suplementos on suplementos.idProd = productos.idProd;
END$$
DELIMITER ;

# Inventario ropa
DELIMITER $$ #
CREATE PROCEDURE  inventario_ropa ()
BEGIN
	SELECT productos.idProd, nombreProd, stock, precioProd, tipo, talla FROM productos RIGHT OUTER JOIN ropa on ropa.idProd = productos.idProd;
END$$
DELIMITER ;

# Inventario accesorios
DELIMITER $$
CREATE PROCEDURE  inventario_accesorios ()
BEGIN
	SELECT * FROM productos LEFT OUTER JOIN ropa ON ropa.idProd = productos.idProd;
END$$
DELIMITER ;

# Iniciar suministro
DELIMITER $$ #
CREATE PROCEDURE iniciar_suministro ()
BEGIN
	INSERT INTO suministra (idProv, fechaSum, horaSum, totalSum) VALUES (1, curdate(), curtime(), 0);
END$$
DELIMITER ;

# Agregar producto
DELIMITER $$
CREATE PROCEDURE agregar_producto(idS INT, idP INT, nombreP VARCHAR(50), precioP FLOAT, stockS INT, estado_venta INT)
BEGIN
	call agregarProducto(idP, nombreP, precioP, stockS, estado_venta);
	set @sub = precioP*stockS;
	insert into detalles_suministra (idSum, idProd, nombreProd, precioSum, cantidadSum, subTotalSum) values (idS, idP, nombreP, precioP, stockS, @sub);
	set @total = (select sum(subTotalSum) from detalles_suministra where idSum = idS);
	update suministra set totalSum = @total where idSum = idS;
END$$
DELIMITER ;

# Agregar producto 2
DELIMITER $$
create procedure agregarProducto (idP INT, nombreP VARCHAR(50), precioP FLOAT, stockS INT, estado_venta INT)
begin
	IF NOT EXISTS ( SELECT idProd FROM productos WHERE idProd = idP ) THEN
		INSERT INTO productos VALUES(idP, nombreP, stockS, precioP, estado_venta);
	ELSE
		update productos set stock = stock + stockS where idProd = idP;
	END IF;
end$$
DELIMITER ;

# Listar venta
DELIMITER $$
CREATE PROCEDURE  listar_venta()
BEGIN
	SELECT * FROM compra where fechaCom = curdate();
END$$
DELIMITER ;

# Lista proveedores
DELIMITER $$ #
CREATE PROCEDURE  listar_proveedor()
BEGIN
	SELECT * FROM proveedor;
END$$
DELIMITER ;

# Modificar membresia
DELIMITER $$ #
CREATE PROCEDURE modificar_membresia (idC INT, idM INT, duracion FLOAT)
BEGIN
	update clientes set idMem = idM where idClien = idC;
	update clientes set duracion = duracion where idclien = idC;
    set @costo = duracion * (SELECT precioMem FROM membresia WHERE idMem = idM);

    select @costo;
END$$
DELIMITER ;

________________
DELIMITER $$
CREATE PROCEDURE  listar_cliente(idc INT)
BEGIN
	SELECT * FROM clientes where idclien = idc;
END$$
DELIMITER $$

DELIMITER $$
CREATE PROCEDURE iniciarCompra (idc int)
BEGIN
	INSERT INTO compra (idClien, fechaCom, horaCom, totalCom) VALUES (idc, curdate(), curtime(), 0); # Creamos una nueva compra, con un total igual a 0
	select last_insert_id(); # Regresamos el ultimo id registrado
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE compra_cliente (idcompra int)
BEGIN
	select idclien from compra where idcom = idcompra;
END$$
DELIMITER ;


DELIMITER $$ #
CREATE PROCEDURE comprar_membresia(idcompra int, idc int, idm int)
BEGIN
	set @duracion = (SELECT duracion from clientes where idclien = idc);
	set @costo = @duracion * (SELECT precioMem FROM membresia WHERE idMem = idM);
	insert into detalles_compras (idCom, idProd, nombreProd, precioProd, cantidadCom, subTotalCom) values (idCompra, 1, 'Membresia', @costo, 1, @costo); # Agregamos un nuevo producto a la lista de compra
    update compra set totalCom = @costo where idCom = idCompra; 
END$$
DELIMITER ;


DELIMITER $$ #
CREATE PROCEDURE eliminar_cliente (idc int)
BEGIN
	delete from clientes where idclien = idc;
END$$
DELIMITER ;


Poner borrado en cascada

DELIMITER $$
CREATE PROCEDURE actualizar_proveedor (ids INT, idp INT)
BEGIN
	UPDATE suministra SET idprov = idp WHERE idsum = ids;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE suministrar_producto(idS INT, idP INT, nombreP VARCHAR(50), precioP FLOAT, stockS INT)
BEGIN
	set @sub = precioP*stockS;
	insert into detalles_suministra (idSum, idProd, nombreProd, precioSum, cantidadSum, subTotalSum) values (idS, idP, nombreP, precioP, stockS, @sub);
	set @total = (select sum(subTotalSum) from detalles_suministra where idSum = idS);
	update suministra set totalSum = @total where idSum = idS;
END$$
DELIMITER ;

# Agregar producto 2
DELIMITER $$
create procedure agregar_bebida (idP INT, nombreP VARCHAR(50), precioP FLOAT, stockS INT, estado_venta INT, cantmili INT)
begin
	IF NOT EXISTS ( SELECT idProd FROM productos WHERE idProd = idP ) THEN
		INSERT INTO productos VALUES(idP, nombreP, stockS, precioP, estado_venta);
		INSERT INTO bebidas VALUES(idP, cantmili);
	ELSE
		update productos set stock = stock + stockS where idProd = idP;
	END IF;
end$$
DELIMITER ;

DELIMITER $$ #
create procedure agregar_suplemento (idP INT, nombreP VARCHAR(50), precioP FLOAT, stockS INT, estado_venta INT, cantgram INT)
begin
	IF NOT EXISTS ( SELECT idProd FROM productos WHERE idProd = idP ) THEN
		INSERT INTO productos VALUES(idP, nombreP, stockS, precioP, estado_venta);
		INSERT INTO suplementos VALUES(idP, cantgram);
	ELSE
		update productos set stock = stock + stockS where idProd = idP;
	END IF;
end$$
DELIMITER ;

DELIMITER $$ #
create procedure agregar_ropa (idP INT, nombreP VARCHAR(50), precioP FLOAT, stockS INT, estado_venta INT, talla VARCHAR(20))
begin
	IF NOT EXISTS ( SELECT idProd FROM productos WHERE idProd = idP ) THEN
		INSERT INTO productos VALUES(idP, nombreP, stockS, precioP, estado_venta);
		INSERT INTO ropa VALUES(idP, 'Desconocido',talla);
	ELSE
		update productos set stock = stock + stockS where idProd = idP;
	END IF;
end$$
DELIMITER ;

DELIMITER $$ #
create procedure agregar_accesorio (idP INT, nombreP VARCHAR(50), precioP FLOAT, stockS INT, estado_venta INT)
begin
	IF NOT EXISTS ( SELECT idProd FROM productos WHERE idProd = idP ) THEN
		INSERT INTO productos VALUES(idP, nombreP, stockS, precioP, estado_venta);
	ELSE
		update productos set stock = stock + stockS where idProd = idP;
	END IF;
end$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE buscar_bebida (idp INT)
BEGIN
	SELECT * from bebidas where idProd = idp;
END$$
DELIMITER ;

# Inventario suplemento
DELIMITER $$
CREATE PROCEDURE buscar_suplemento (idp INT)
BEGIN
	SELECT * from suplementos where idProd = idp;
END$$
DELIMITER ;

# Inventario ropa
DELIMITER $$
CREATE PROCEDURE  buscar_ropa (idp INT)
BEGIN
SELECT * from ropa where idProd = idp;
END$$
DELIMITER ;

# Inventario accesorios
DELIMITER $$ #
CREATE PROCEDURE  inventario_accesorios ()
BEGIN
	SELECT * FROM productos LEFT OUTER JOIN ropa ON ropa.idProd = productos.idProd;
END$$
DELIMITER ;


DELIMITER $$ 
CREATE PROCEDURE actualizar_bebida (idp INT, nombreP VARCHAR(50), precioP FLOAT, estado INT, cantmili INT)
BEGIN
	UPDATE productos set nombreprod=nombreP, precioProd=precioP, estado_venta=estado where idprod=idp;
	UPDATE bebidas set cantidadMililitros=cantmili where idProd=idp;
END$$
DELIMITER ;

DELIMITER $$ 
CREATE PROCEDURE actualizar_suplemento (idp INT, nombreP VARCHAR(50), precioP FLOAT, estado INT, cantgram INT)
BEGIN
	UPDATE productos set nombreprod=nombreP, precioProd=precioP, estado_venta=estado where idprod=idp;
	UPDATE suplementos set cantidadGramos=cantgram where idProd=idp;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE actualizar_ropa (idp INT, nombreP VARCHAR(50), precioP FLOAT, estado INT, tallaP VARCHAR(20))
BEGIN
	UPDATE productos set nombreprod=nombreP, precioProd=precioP, estado_venta=estado where idprod=idp;
	UPDATE ropa set talla=tallaP where idProd=idp;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE actualizar_accesorio (idp INT, nombreP VARCHAR(50), precioP FLOAT, estado INT)
BEGIN
	UPDATE productos set nombreprod=nombreP, precioProd=precioP, estado_venta=estado where idprod=idp;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE eliminar_producto (idp int)
BEGIN
	delete from bebidas where idProd = idp;
	delete from suplementos where idProd = idp;
	delete from ropa where idProd = idp;
	delete from productos where idProd = idp;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE agregar_proveedor (idp int, nombre VARCHAR(50), tel VARCHAR(12))
BEGIN
	INSERT INTO proveedor VALUES (idp, nombre, tel);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE actualiza_proveedor (idp int, nombre VARCHAR(50), tel VARCHAR(12))
BEGIN
	UPDATE proveedor set nombreprov = nombre, telefono = tel WHERE idProv = idp;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE elimina_proveedor (idp int)
BEGIN
	delete from proveedor where idProv = idp;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE total_compra_diaria ()
BEGIN
	SELECT sum(totalcom) FROM compra where fechaCom = curdate();
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE contar_clientes ()
BEGIN
	SELECT count(idclien) FROM clientes;
END$$
DELIMITER ;