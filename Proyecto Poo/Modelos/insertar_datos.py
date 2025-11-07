from Prueba_102025.conexion import sesion

def actualizar_producto(producto):
    sesion.add(producto)
    try:
        sesion.commit()
        print('Se actualizo el producto correctamente')
    except Exception as e:
        sesion.rollback()
        print('Intentalo de nuevo')
    finally:
        sesion.close

def actualizar_producto(produto):
    sesion.merge(produto)
    try:
        sesion.commit()
        print("El producto se ha actualizado correctamente.")
    except Exception as e:
        sesion.rollback()
        print(f"Error al actualizar el producto: {e}")
    finally:
        sesion.close()