# src/pagos.py

class ProcesadorPagos:
    def __init__(self, limite_diario=5000, monto_minimo=1):
        self.limite_diario = limite_diario
        self.monto_minimo = monto_minimo
        self.total_procesado_hoy = 0

    def calcular_impuesto(self, monto, tasa=0.18):
        """Calcula el impuesto según la tasa (18% por defecto)"""
        return monto * tasa

    def validar_pago(self, monto):
        """Valida si el pago cumple con montos mínimo y límite diario"""
        if monto < self.monto_minimo:
            return False, f"Monto {monto} es menor al mínimo permitido ({self.monto_minimo})"
        
        if self.total_procesado_hoy + monto > self.limite_diario:
            return False, f"Supera el límite diario de {self.limite_diario}"
        
        return True, "OK"

    def procesar_pago(self, monto):
        """Procesa un pago, aplica impuesto y actualiza el total diario"""
        valido, mensaje = self.validar_pago(monto)
        if not valido:
            return {"exito": False, "mensaje": mensaje}
        
        impuesto = self.calcular_impuesto(monto)
        self.total_procesado_hoy += monto
        
        return {
            "exito": True, 
            "monto": monto, 
            "impuesto": impuesto, 
            "total": monto + impuesto
        }

    def procesar_reembolso(self, monto_original, politica="completo"):
        """Procesa reembolsos según política: completo, parcial o ninguno"""
        if politica == "completo":
            return monto_original
        elif politica == "parcial":
            return monto_original * 0.5
        else:
            return 0

    def reiniciar_dia(self):
        """Reinicia el contador diario (para pruebas)"""
        self.total_procesado_hoy = 0