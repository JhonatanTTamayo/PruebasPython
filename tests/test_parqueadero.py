import pytest
from datetime import datetime, timedelta
from parqueadero.parqueadero import Parqueadero
from parqueadero.vehiculo import Vehiculo

# Fixtures para reutilizar objetos en múltiples pruebas
@pytest.fixture
def parqueadero():
    return Parqueadero(capacidad=3)

@pytest.fixture
def vehiculo_carro():
    return Vehiculo(placa="ABC123", tipo="carro")

@pytest.fixture
def vehiculo_moto():
    return Vehiculo(placa="XYZ789", tipo="moto")

# --- Pruebas para registrar_entrada ---
def test_registrar_entrada_vehiculo_valido(parqueadero, vehiculo_carro):
    parqueadero.registrar_entrada(vehiculo_carro)
    assert parqueadero.espacios_ocupados == 1
    assert "ABC123" in parqueadero.vehiculos

def test_registrar_entrada_vehiculo_duplicado(parqueadero, vehiculo_carro):
    parqueadero.registrar_entrada(vehiculo_carro)
    with pytest.raises(ValueError, match="Vehículo ya registrado"):
        parqueadero.registrar_entrada(vehiculo_carro)

def test_registrar_entrada_parqueadero_lleno(parqueadero):
    for i in range(3):
        vehiculo = Vehiculo(placa=f"VEH{i}", tipo="carro")
        parqueadero.registrar_entrada(vehiculo)
    vehiculo_extra = Vehiculo(placa="EXTRA", tipo="moto")
    with pytest.raises(ValueError, match="Parqueadero lleno"):
        parqueadero.registrar_entrada(vehiculo_extra)

# --- Pruebas para registrar_salida ---
def test_registrar_salida_vehiculo_existente(parqueadero, vehiculo_carro):
    parqueadero.registrar_entrada(vehiculo_carro)
    vehiculo_carro.hora_entrada = datetime.now() - timedelta(hours=2)
    costo = parqueadero.registrar_salida("ABC123")
    assert costo == 20  # 2 horas * $10/hora
    assert parqueadero.espacios_ocupados == 0

def test_registrar_salida_vehiculo_inexistente(parqueadero):
    with pytest.raises(ValueError, match="Vehículo no encontrado"):
        parqueadero.registrar_salida("NO_EXISTE")

# --- Pruebas para calcular_costo ---
@pytest.mark.parametrize("tipo, horas, costo_esperado", [
    ("carro", 1.5, 15.0),   # 1.5 horas * $10 = $15
    ("moto", 3.25, 16.25),  # 3.25 horas * $5 = $16.25
    ("bicicleta", 0.5, 1.0),# 0.5 horas * $2 = $1
    ("camion", 2, 16.0),    # 2 horas * $8 (tarifa por defecto) = $16
])
def test_calcular_costo(tipo, horas, costo_esperado, parqueadero):
    vehiculo = Vehiculo(placa="TEST", tipo=tipo)
    vehiculo.hora_entrada = datetime.now() - timedelta(hours=horas)
    vehiculo.hora_salida = datetime.now()
    costo = parqueadero.calcular_costo(vehiculo)
    assert costo == pytest.approx(costo_esperado, 0.01)  # Tolerancia de 0.01

def test_calcular_costo_sin_horas(parqueadero, vehiculo_carro):
    with pytest.raises(ValueError, match="Horas de entrada o salida no registradas"):
        parqueadero.calcular_costo(vehiculo_carro)

# --- Pruebas para generar_reporte ---
def test_generar_reporte_sin_vehiculos(parqueadero):
    reporte = parqueadero.generar_reporte()
    assert reporte["espacios_disponibles"] == 3
    assert len(reporte["vehiculos_estacionados"]) == 0
    assert reporte["total_recaudado"] == 0

def test_generar_reporte_con_vehiculos_activos(parqueadero, vehiculo_carro, vehiculo_moto):
    parqueadero.registrar_entrada(vehiculo_carro)
    parqueadero.registrar_entrada(vehiculo_moto)
    reporte = parqueadero.generar_reporte()
    assert "En estacionamiento" in reporte["vehiculos_estacionados"][0]
    assert "En estacionamiento" in reporte["vehiculos_estacionados"][1]

def test_generar_reporte_con_tiempo_estacionado(parqueadero, vehiculo_carro):
    parqueadero.registrar_entrada(vehiculo_carro)
    vehiculo_carro.hora_entrada = datetime.now() - timedelta(hours=2, minutes=30)
    vehiculo_carro.hora_salida = datetime.now()
    reporte = parqueadero.generar_reporte()
    assert "Tiempo estacionado: 2h 30m 0s" in reporte["vehiculos_estacionados"][0]

# --- Pruebas para formatear_tiempo ---
def test_formatear_tiempo(parqueadero):
    tiempo = timedelta(hours=2, minutes=30, seconds=15)
    tiempo_formateado = parqueadero.formatear_tiempo(tiempo)
    assert tiempo_formateado == "2h 30m 15s"