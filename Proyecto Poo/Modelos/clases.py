from datetime import datetime
from enum import Enum
from typing import List, Optional

class EstadoPedido(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADO = "CONFIRMADO"
    EN_PROCESO = "EN_PROCESO"
    ENVIADO = "ENVIADO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"


class MetodoPago(Enum):
    TARJETA_CREDITO = "TARJETA_CREDITO"
    TARJETA_DEBITO = "TARJETA_DEBITO"
    TRANSFERENCIA_BANCARIA = "TRANSFERENCIA_BANCARIA"

class EstadoPago(Enum):
    PENDIENTE = "PENDIENTE"
    PROCESANDO = "PROCESANDO"
    COMPLETADO = "COMPLETADO"
    RECHAZADO = "RECHAZADO"
    REEMBOLSADO = "REEMBOLSADO"

class EstadoProducto(Enum):
    DISPONIBLE = "DISPONIBLE"
    AGOTADO = "AGOTADO"
    DESCONTINUADO = "DESCONTINUADO"
    PROMOCION = "PROMOCION"

class Cliente:
    def __init__(self, id: str, nombre: str, email: str, telefono: str, direccion: str):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
    
    def registrar_cliente(self) -> bool:
        """Registra al cliente en el sistema"""
        print(f"Cliente {self.nombre} registrado exitosamente")
        return True
    
    def realizar_pedido(self) -> 'Pedido':
        """Crea un nuevo pedido para este cliente"""
        pedido = Pedido(
            id=f"PED_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            fecha=datetime.now(),
            estado=EstadoPedido.PENDIENTE,
            total=0.0,
            cliente=self
        )
        print(f"Pedido {pedido.id} creado para el cliente {self.nombre}")
        return pedido
    
    def __str__(self):
        return f"Cliente[id={self.id}, nombre={self.nombre}, email={self.email}]"

class Producto:
    def __init__(self, id: str, nombre: str, descripcion: str, precio: float, stock: int, estado: EstadoProducto = EstadoProducto.DISPONIBLE):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.estado = estado
    
    def actualizar_stock(self, cantidad: int) -> bool:
        """Actualiza el stock del producto"""
        nuevo_stock = self.stock + cantidad
        if nuevo_stock >= 0:
            self.stock = nuevo_stock
            
            # Actualizar estado basado en el stock
            if self.stock == 0:
                self.estado = EstadoProducto.AGOTADO
            elif self.stock > 0 and self.estado == EstadoProducto.AGOTADO:
                self.estado = EstadoProducto.DISPONIBLE
            
            print(f"Stock de {self.nombre} actualizado a {self.stock}")
            return True
        else:
            print(f"Error: No hay suficiente stock para reducir {cantidad} unidades")
            return False
    
    def verificar_stock(self, cantidad: int) -> bool:
        """Verifica si hay suficiente stock disponible"""
        disponible = self.stock >= cantidad and self.estado in [EstadoProducto.DISPONIBLE, EstadoProducto.PROMOCION]
        print(f"Stock verificado para {self.nombre}: {cantidad} {'disponible' if disponible else 'no disponible'}")
        return disponible
    
    def calcular_precio_total(self, cantidad: int) -> float:
        """Calcula el precio total para una cantidad dada"""
        if cantidad <= 0:
            return 0.0
        
        total = self.precio * cantidad
        # Aquí se podrían aplicar descuentos si el producto está en promoción
        if self.estado == EstadoProducto.PROMOCION:
            # Aplicar 10% de descuento para productos en promoción
            total *= 0.9
        
        return round(total, 2)
    
    def __str__(self):
        return f"Producto[id={self.id}, nombre={self.nombre}, precio=${self.precio}, stock={self.stock}, estado={self.estado.value}]"

class ItemPedido:
    def __init__(self, id: str, producto: Producto, cantidad: int, precio_unitario: float = None):
        self.id = id
        self.producto = producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario if precio_unitario is not None else producto.precio
        self.subtotal = self.calcular_subtotal()
    
    def calcular_subtotal(self) -> float:
        """Calcula el subtotal del item"""
        self.subtotal = round(self.precio_unitario * self.cantidad, 2)
        return self.subtotal
    
    def actualizar_cantidad(self, nueva_cantidad: int) -> bool:
        """Actualiza la cantidad del item"""
        if nueva_cantidad > 0:
            self.cantidad = nueva_cantidad
            self.calcular_subtotal()
            print(f"Cantidad actualizada a {nueva_cantidad} para {self.producto.nombre}")
            return True
        else:
            print("Error: La cantidad debe ser mayor a 0")
            return False
    
    def __str__(self):
        return f"ItemPedido[id={self.id}, producto={self.producto.nombre}, cantidad={self.cantidad}, subtotal=${self.subtotal}]"

class Pedido:
    def __init__(self, id: str, fecha: datetime, estado: EstadoPedido, total: float, cliente: Cliente):
        self.id = id
        self.fecha = fecha
        self.estado = estado
        self.total = total
        self.cliente = cliente
        self.items: List[ItemPedido] = []
    
    def calcular_total(self) -> float:
        """Calcula el total del pedido sumando todos los items"""
        self.total = round(sum(item.calcular_subtotal() for item in self.items), 2)
        return self.total
    
    def actualizar_estado(self, nuevo_estado: EstadoPedido):
        """Actualiza el estado del pedido"""
        estado_anterior = self.estado
        self.estado = nuevo_estado
        print(f"Pedido {self.id} cambió de {estado_anterior.value} a {nuevo_estado.value}")
    
    def agregar_producto(self, producto: Producto, cantidad: int) -> bool:
        """Agrega un producto al pedido"""
        if not producto.verificar_stock(cantidad):
            print(f"No se puede agregar {producto.nombre} - Stock insuficiente")
            return False
        
        # Verificar si el producto ya está en el pedido
        for item in self.items:
            if item.producto.id == producto.id:
                # Actualizar cantidad si ya existe
                return item.actualizar_cantidad(item.cantidad + cantidad)
        
        # Crear nuevo item
        nuevo_item = ItemPedido(
            id=f"ITEM_{len(self.items) + 1}",
            producto=producto,
            cantidad=cantidad
        )
        self.items.append(nuevo_item)
        self.calcular_total()
        print(f"Producto {producto.nombre} agregado al pedido")
        return True
    
    def procesar_pedido(self) -> bool:
        """Procesa el pedido completo"""
        if self.estado != EstadoPedido.PENDIENTE:
            print(f"No se puede procesar el pedido. Estado actual: {self.estado.value}")
            return False
        
        # Verificar stock para todos los items
        for item in self.items:
            if not item.producto.verificar_stock(item.cantidad):
                print(f"Stock insuficiente para {item.producto.nombre}")
                return False
        
        # Actualizar stock y estado
        for item in self.items:
            item.producto.actualizar_stock(-item.cantidad)
        
        self.actualizar_estado(EstadoPedido.CONFIRMADO)
        print(f"Pedido {self.id} procesado exitosamente")
        return True
    
    def __str__(self):
        return f"Pedido[id={self.id}, fecha={self.fecha.strftime('%Y-%m-%d %H:%M')}, estado={self.estado.value}, total=${self.total}, cliente={self.cliente.nombre}]"

class Pago:
    def __init__(self, id: str, monto: float, fecha: datetime, metodo: MetodoPago, estado: EstadoPago = EstadoPago.PENDIENTE):
        self.id = id
        self.monto = monto
        self.fecha = fecha
        self.metodo = metodo
        self.estado = estado
    
    def procesar_pago(self) -> bool:
        """Procesa el pago"""
        if self.estado != EstadoPago.PENDIENTE:
            print(f"El pago ya fue procesado. Estado actual: {self.estado.value}")
            return False
        
        self.estado = EstadoPago.PROCESANDO
        print(f"Procesando pago {self.id}...")
        
        # Simular procesamiento
        # En una implementación real, aquí se conectaría con la pasarela de pago
        import random
        exito = random.choice([True, False])  # Simular éxito/fallo aleatorio
        
        if exito:
            self.estado = EstadoPago.COMPLETADO
            print(f"Pago {self.id} procesado exitosamente")
        else:
            self.estado = EstadoPago.RECHAZADO
            print(f"Pago {self.id} rechazado")
        
        return exito
    
    def verificar_estado(self) -> EstadoPago:
        """Verifica el estado actual del pago"""
        return self.estado
    
    def __str__(self):
        return f"Pago[id={self.id}, monto=${self.monto}, metodo={self.metodo.value}, estado={self.estado.value}]"

# Ejemplo de uso del sistema
if __name__ == "__main__":
    # Crear cliente
    cliente = Cliente(
        id="CLI_001",
        nombre="Juan Pérez",
        email="juan@email.com",
        telefono="+123456789",
        direccion="Calle Principal 123"
    )
    cliente.registrar_cliente()
    
    # Crear productos
    producto1 = Producto(
        id="PROD_001",
        nombre="Laptop Gaming",
        descripcion="Laptop para gaming de alta gama",
        precio=1200.00,
        stock=10
    )
    
    producto2 = Producto(
        id="PROD_002",
        nombre="Mouse Inalámbrico",
        descripcion="Mouse ergonómico inalámbrico",
        precio=45.50,
        stock=25,
        estado=EstadoProducto.PROMOCION
    )
    
    # Cliente realiza pedido
    pedido = cliente.realizar_pedido()
    
    # Agregar productos al pedido
    pedido.agregar_producto(producto1, 1)
    pedido.agregar_producto(producto2, 2)
    
    print(f"\nResumen del pedido:")
    print(pedido)
    for item in pedido.items:
        print(f"  - {item}")
    
    # Procesar pedido
    if pedido.procesar_pedido():
        # Crear y procesar pago
        pago = Pago(
            id=f"PAGO_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            monto=pedido.total,
            fecha=datetime.now(),
            metodo=MetodoPago.TARJETA_CREDITO
        )
        
        print(f"\nProcesando pago...")
        pago.procesar_pago()
        print(pago)
    
    print(f"\nEstado final de productos:")
    print(producto1)
    print(producto2)