# parqueadero/parqueadero.py
from datetime import datetime, timedelta
from .vehiculo import Vehiculo  # Importar la clase Vehiculo desde el mismo paquete

class Parqueadero:
    def __init__(self, capacidad):
        """
        Inicializa el parqueadero con una capacidad máxima.
        :param capacidad: Número máximo de vehículos que puede albergar el parqueadero (int).
        """
        self.capacidad = capacidad
        self.espacios_ocupados = 0
        self.vehiculos = {}  # Diccionario para guardar los vehículos por placa

    def registrar_entrada(self, vehiculo):
        """
        Registra la entrada de un vehículo al parqueadero.
        :param vehiculo: Objeto de tipo Vehiculo.
        :raises ValueError: Si el parqueadero está lleno o el vehículo ya está registrado.
        """
        if self.espacios_ocupados >= self.capacidad:
            raise ValueError("Parqueadero lleno")
        if vehiculo.placa in self.vehiculos:
            raise ValueError("Vehículo ya registrado")
        vehiculo.hora_entrada = datetime.now()
        self.vehiculos[vehiculo.placa] = vehiculo
        self.espacios_ocupados += 1

    def registrar_salida(self, placa):
        """
        Registra la salida de un vehículo del parqueadero y calcula el costo.
        :param placa: Placa del vehículo que sale (str).
        :return: Costo del estacionamiento (float).
        :raises ValueError: Si el vehículo no está registrado.
        """
        if placa not in self.vehiculos:
            raise ValueError("Vehículo no encontrado")
        vehiculo = self.vehiculos[placa]
        vehiculo.hora_salida = datetime.now()
        self.espacios_ocupados -= 1
        return self.calcular_costo(vehiculo)

    def calcular_costo(self, vehiculo):
        """
        Calcula el costo del estacionamiento basado en el tiempo y el tipo de vehículo.
        :param vehiculo: Objeto de tipo Vehiculo.
        :return: Costo del estacionamiento (float).
        :raises ValueError: Si no se han registrado las horas de entrada o salida.
        """
        if not vehiculo.hora_entrada or not vehiculo.hora_salida:
            raise ValueError("Horas de entrada o salida no registradas")
        tiempo_estacionado = vehiculo.hora_salida - vehiculo.hora_entrada
        horas_estacionado = tiempo_estacionado.total_seconds() / 3600

        tarifas = {
            "carro": 10,
            "moto": 5,
            "bicicleta": 2,
        }
        tarifa = tarifas.get(vehiculo.tipo, 8)  # Tarifa por defecto: $8
        return round(horas_estacionado * tarifa, 2)

    def espacios_disponibles(self):
        """
        Devuelve el número de espacios disponibles en el parqueadero.
        :return: Espacios disponibles (int).
        """
        return self.capacidad - self.espacios_ocupados

    def formatear_tiempo(self, tiempo_estacionado):
        """
        Formatea el tiempo de estacionamiento en un formato legible (horas, minutos, segundos).
        :param tiempo_estacionado: Objeto timedelta que representa el tiempo estacionado.
        :return: Tiempo formateado como una cadena (str).
        """
        horas = int(tiempo_estacionado.total_seconds() // 3600)
        minutos = int((tiempo_estacionado.total_seconds() % 3600) // 60)
        segundos = int(tiempo_estacionado.total_seconds() % 60)
        return f"{horas}h {minutos}m {segundos}s"

    def generar_reporte(self):
        """
        Genera un reporte del estado actual del parqueadero.
        :return: Diccionario con espacios disponibles, vehículos estacionados, tiempo estacionado y total recaudado.
        """
        reporte = {
            "espacios_disponibles": self.espacios_disponibles(),
            "vehiculos_estacionados": [],
            "total_recaudado": sum(
                self.calcular_costo(v) for v in self.vehiculos.values() if v.hora_salida
            ),
        }

        # Agregar información detallada de cada vehículo
        for vehiculo in self.vehiculos.values():
            if vehiculo.hora_salida:
                tiempo_estacionado = vehiculo.hora_salida - vehiculo.hora_entrada
                tiempo_formateado = self.formatear_tiempo(tiempo_estacionado)
                reporte["vehiculos_estacionados"].append(
                    f"{vehiculo} - Tiempo estacionado: {tiempo_formateado}"
                )
            else:
                reporte["vehiculos_estacionados"].append(f"{vehiculo} - En estacionamiento")

        return reporte