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
CREATE PROCEDURE iniciarCom()
BEGIN
	INSERT INTO compra (idClien, fechaCom, horaCom, totalCom) VALUES (1, curdate(), curtime(), 0); # Creamos una nueva compra, con un total igual a 0
	select last_insert_id(); # Regresamos el ultimo id registrado
END$$
DELIMITER ;

# Agregar producto
DELIMITER $$
CREATE PROCEDURE agregarProd(idCompra INT, idProducto INT, cantidad INT)
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
CREATE PROCEDURE reducirStock(idProducto INT, cantidad INT)
BEGIN
	UPDATE productos SET stock = stock-cantidad WHERE idProd = idProducto; # Disminuimos el stock dependiendo de la cantidad comprada
END$$
DELIMITER ;

# Buscar compra
DELIMITER $$
CREATE PROCEDURE buscarCom(id INT)
BEGIN
	SELECT * FROM compra WHERE idCom = id; # Busca una compra en especifico
END$$
DELIMITER ;

# Buscar detalle compra
DELIMITER $$
CREATE PROCEDURE buscarDtCom(id INT)
BEGIN
	SELECT * FROM detalles_compras WHERE idCom = id; # Busca los productos comprados detalladamente de una compra general
END$$
DELIMITER ;

# Buscar producto
DELIMITER $$
CREATE PROCEDURE buscarProd(id INT)
BEGIN
	SELECT * FROM productos WHERE idProd = id; # Buscamos un preducto en especifico
END$$
DELIMITER ;