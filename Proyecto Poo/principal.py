from Prueba_102025.Modelos.Clases import EstadoPedido, EstadoPago,EstadoProducto,Producto,MetodoPago,Cliente,ItemPedido,Pedido,Pago
from Prueba_102025.conexion import sesion
from sqlalchemy import func



def guardar_marca(nombre,precio):
    if Producto != '':
        nuevo_producto = nuevo_producto(
            precio=precio,
            nombre_producto=nombre.title())
        sesion.add(nuevo_producto)
        try:
            sesion.commit()
            print(
                f"El producto '{nuevo_producto.nombre_producto}' se ha guardado correctamente.")
        except Exception as e:
            sesion.rollback()
            print(f"Error al guardar el producto: {e}")
        finally:
            sesion.close()
    else:
        print('Debe ingresar el nombre del producto.')