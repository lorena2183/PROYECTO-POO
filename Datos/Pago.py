class Pago:
    def __init__(self, id_pago, monto, metodo):
    self.id_pago = id_pago
    self.monto = monto
    self.metodo = metodo 
    self.estado = "PENDIENTE"

    def procesar_pago (self):
        if self.monto >0:
            self.estado = "COMPLETADO"
            return True
        else:
            estado = "RECHAZADO"
            return False

    def verificar_estado(self):
        return self.estado



class MetodoPago: 
    Tarjeta_Credito = "Tarjeta_Credito"
    Tarjeta_Debito = "Tarjeta_Debito"
    Transferencia_Bancaria = "Transferencia_Bancaria"
    
    def todos_metodos():
        return [
            MetodoPago.Tarjeta_Credito,
            MetodoPago.Tarjeta_Debito,
            MetodoPago.Transferencia_Bancaria
            ]



    class EstadoPago:
        Pendiente = "Pendiente"
        Procesando = "Procesando"
        Completado = "Completado"
        Rechazado = "Rechazado"
        Reembolsado = "Rembolsado"

        def todos_estados():
            return [
                EstadoPago.Pendiente,
                EstadoPago.Procesando,
                EstadoPago.Completado,
                EstadoPago.Rechazado,
                EstadoPago.Reembolsado
                ] 