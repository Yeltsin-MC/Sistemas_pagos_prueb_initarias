
import pytest
from src.pagos import ProcesadorPagos

# PRUEBAS PARA CÁLCULO DE IMPUESTOS

def test_calcular_impuesto_monto_normal():
    
    pagos = ProcesadorPagos()
    
    impuesto = pagos.calcular_impuesto(100)
    
    assert impuesto == 18.0

def test_calcular_impuesto_monto_cero():
    pagos = ProcesadorPagos()
    impuesto = pagos.calcular_impuesto(0)
    assert impuesto == 0.0

def test_calcular_impuesto_con_tasa_personalizada():
    pagos = ProcesadorPagos()
    impuesto = pagos.calcular_impuesto(100, tasa=0.10)
    assert impuesto == 10.0

# PRUEBAS PARA VALIDACIÓN DE PAGOS

def test_pago_menor_al_minimo():
    pagos = ProcesadorPagos(monto_minimo=10)
    resultado = pagos.procesar_pago(5)
    assert resultado["exito"] is False
    assert "menor al mínimo" in resultado["mensaje"]

def test_pago_monto_minimo_exacto():
    pagos = ProcesadorPagos(monto_minimo=10)
    resultado = pagos.procesar_pago(10)
    assert resultado["exito"] is True
    assert resultado["monto"] == 10

def test_pago_respeta_limite_diario():
    pagos = ProcesadorPagos(limite_diario=100)
    pagos.reiniciar_dia()
    
    # Primer pago de 60 - debe pasar
    resultado1 = pagos.procesar_pago(60)
    assert resultado1["exito"] is True
    
    # Segundo pago de 50 - excede el límite (60+50=110 > 100)
    resultado2 = pagos.procesar_pago(50)
    assert resultado2["exito"] is False
    assert "límite diario" in resultado2["mensaje"]

def test_pago_exacto_en_limite():
    pagos = ProcesadorPagos(limite_diario=100)
    pagos.reiniciar_dia()
    
    resultado = pagos.procesar_pago(100)
    assert resultado["exito"] is True

def test_pago_con_total_correcto():
    pagos = ProcesadorPagos()
    pagos.reiniciar_dia()
    
    resultado = pagos.procesar_pago(100)
    assert resultado["exito"] is True
    assert resultado["monto"] == 100
    assert resultado["impuesto"] == 18.0
    assert resultado["total"] == 118.0

# PRUEBAS PARA REEMBOLSOS

def test_reembolso_completo():
    pagos = ProcesadorPagos()
    reembolso = pagos.procesar_reembolso(100, "completo")
    assert reembolso == 100

def test_reembolso_parcial():
    pagos = ProcesadorPagos()
    reembolso = pagos.procesar_reembolso(100, "parcial")
    assert reembolso == 50

def test_reembolso_sin_politica():
    pagos = ProcesadorPagos()
    reembolso = pagos.procesar_reembolso(100, "ninguna")
    assert reembolso == 0

def test_reembolso_politica_por_defecto():
    pagos = ProcesadorPagos()
    reembolso = pagos.procesar_reembolso(100)
    assert reembolso == 100  # Por defecto es "completo"

# PRUEBAS DE LÍMITES (Boundary Testing)

def test_limite_monto_minimo_justo():
    pagos = ProcesadorPagos(monto_minimo=10)
    
    # Valores límite: 9 (falla), 10 (pasa)
    resultado_falla = pagos.procesar_pago(9)
    resultado_pasa = pagos.procesar_pago(10)
    
    assert resultado_falla["exito"] is False
    assert resultado_pasa["exito"] is True

def test_limite_diario_justo():
    pagos = ProcesadorPagos(limite_diario=100)
    pagos.reiniciar_dia()
    
    # 99 (pasa), 100 (pasa justo), 101 (falla)
    assert pagos.procesar_pago(99)["exito"] is True
    pagos.reiniciar_dia()
    assert pagos.procesar_pago(100)["exito"] is True
    pagos.reiniciar_dia()
    assert pagos.procesar_pago(101)["exito"] is False