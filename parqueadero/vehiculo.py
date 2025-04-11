class Vehiculo:
    """
    Clase que representa un vehículo en el sistema de parqueadero.
    """

    def __init__(self, placa, tipo):
        """
        Inicializa un vehículo con placa y tipo.
        :param placa: Número de placa del vehículo (str).
        :param tipo: Tipo de vehículo (str): "carro", "moto", "bicicleta".
        """
        self.placa = placa
        self.tipo = tipo
        self.hora_entrada = None  # Hora de entrada al parqueadero
        self.hora_salida = None   # Hora de salida del parqueadero

    def __str__(self):
        """
        Representación en cadena del vehículo.
        """
        return f"Vehículo {self.tipo} con placa {self.placa}"
