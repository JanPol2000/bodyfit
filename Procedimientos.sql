# Procedimientos
# Ejemplo
# delimiter $$
# create procedure mostrarProductos()
# begin
# 	select * from productos;
# end$$
# delimiter ;

# Iniciar compra
DELIMITER $$
CREATE PROCEDURE iniciarCom ()
BEGIN
	INSERT INTO compra (idClien, fechaCom, horaCom, totalCom) VALUES (1, curdate(), curtime(), 0); # Creamos una nueva compra, con un total igual a 0
	select last_insert_id(); # Regresamos el ultimo id registrado
END$$
DELIMITER ;

# Agregar producto
DELIMITER $$
CREATE PROCEDURE agregarProd (idCompra INT, idProducto INT, cantidad INT)
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
CREATE PROCEDURE reducirStock (idProducto INT, cantidad INT)
BEGIN
	UPDATE productos SET stock = stock-cantidad WHERE idProd = idProducto; # Disminuimos el stock dependiendo de la cantidad comprada
END$$
DELIMITER ;

# Buscar compra
DELIMITER $$
CREATE PROCEDURE buscarCom (id INT)
BEGIN
	SELECT * FROM compra WHERE idCom = id; # Busca una compra en especifico
END$$
DELIMITER ;

# Buscar detalle compra
DELIMITER $$
CREATE PROCEDURE buscarDtCom (id INT)
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
DELIMITER $$
CREATE PROCEDURE agregar_cliente (nombreC VARCHAR (20), apellidoP VARCHAR (20), apellidoM VARCHAR (20), apodo VARCHAR (15), duracion INT, idM INT)
BEGIN
	INSERT INTO clientes VALUES (idM, nombreC, apellidoP, apellidoM, apodo, duracion);
	set @costo = duracion * (SELECT precioMem FROM membresia WHERE idMem = idM);
    select @costo;
END$$
DELIMITER ;

# Inventario general
DELIMITER $$
CREATE PROCEDURE inventario_general ()
BEGIN
	SELECT * FROM productos;
END$$
DELIMITER ;

# Inventario bebidas
DELIMITER $$
CREATE PROCEDURE inventario_bebidas ()
BEGIN
	SELECT productos.idProd, nombreProd, stock, precioProd, cantidadMililitros FROM productos RIGHT OUTER JOIN bebidas on bebidas.idProd = productos.idProd;
END$$
DELIMITER $$

# Inventario suplemento
DELIMITER $$
CREATE PROCEDURE inventario_suplementos ()
BEGIN
	SELECT productos.idProd, nombreProd, stock, precioProd, cantidadGramos FROM productos RIGHT OUTER JOIN suplementos on suplementos.idProd = productos.idProd;
END$$
DELIMITER $$

# Inventario ropa
DELIMITER $$
CREATE PROCEDURE  inventario_ropa ()
BEGIN
	SELECT productos.idProd, nombreProd, stock, precioProd, tipo, talla FROM productos RIGHT OUTER JOIN ropa on ropa.idProd = productos.idProd;
END$$
DELIMITER $$

# Inventario accesorios
DELIMITER $$
CREATE PROCEDURE  inventario_accesorio ()
BEGIN
	SELECT * FROM productos LEFT OUTER JOIN ropa ON ropa.idProd = productos.idProd;
END$$
DELIMITER $$

# Iniciar suministro
DELIMITER $$
CREATE PROCEDURE iniciar_suministro (id INT, fechaS DATE, horaS TIME)
BEGIN
	INSERT INTO suministra (idProv, fechaSum, horaSum, totalSum) VALUES (1, curdate(), curtime(), 0);
	select last_insert_id();
END$$
DELIMITER $$

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
DELIMITER $$

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
DELIMITER $$

# Lista proveedores
DELIMITER $$
CREATE PROCEDURE  lista_proveedor()
BEGIN
	SELECT * FROM proveedor;
END$$
DELIMITER $$

# Modificar membresia
DELIMITER $$
CREATE PROCEDURE modificar_membresia (idC INT, idM INT, duracion INT)
BEGIN
	update clientes set idMem = idM where idClien = idM;
    set @costo = duracion * (SELECT precioMem FROM membresia WHERE idMem = idM);
    select @costo;
END$$
DELIMITER $$
