# parqueadero/interfaz.py
import tkinter as tk
from tkinter import messagebox
from .parqueadero import Parqueadero
from .vehiculo import Vehiculo

class InterfazParqueadero:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Parqueadero")
        self.parqueadero = Parqueadero(capacidad=10)

        # Configurar la interfaz
        self.configurar_interfaz()

    def configurar_interfaz(self):
        """
        Configura todos los componentes de la interfaz gráfica.
        """
        # Título
        self.crear_titulo()

        # Campos de entrada
        self.crear_campos_entrada()

        # Botones
        self.crear_botones()

    def crear_titulo(self):
        """
        Crea el título de la interfaz.
        """
        self.label = tk.Label(
            self.root, 
            text="Bienvenido al Parqueadero", 
            font=("Arial", 16)
        )
        self.label.pack(pady=10)

    def crear_campos_entrada(self):
        """
        Crea los campos de entrada para la placa y el tipo de vehículo.
        """
        self.frame_entrada = tk.Frame(self.root)
        self.frame_entrada.pack(pady=10)

        # Campo para la placa
        self.placa_label = tk.Label(self.frame_entrada, text="Placa:")
        self.placa_label.grid(row=0, column=0, padx=5, pady=5)
        self.placa_entry = tk.Entry(self.frame_entrada)
        self.placa_entry.grid(row=0, column=1, padx=5, pady=5)

        # Campo para el tipo de vehículo
        self.tipo_label = tk.Label(self.frame_entrada, text="Tipo (carro, moto, bicicleta):")
        self.tipo_label.grid(row=1, column=0, padx=5, pady=5)
        self.tipo_entry = tk.Entry(self.frame_entrada)
        self.tipo_entry.grid(row=1, column=1, padx=5, pady=5)

    def crear_botones(self):
        """
        Crea los botones de la interfaz.
        """
        self.frame_botones = tk.Frame(self.root)
        self.frame_botones.pack(pady=10)

        # Botón para registrar entrada
        self.registrar_entrada_button = tk.Button(
            self.frame_botones, 
            text="Registrar Entrada", 
            command=self.registrar_entrada
        )
        self.registrar_entrada_button.grid(row=0, column=0, padx=5, pady=5)

        # Botón para registrar salida
        self.registrar_salida_button = tk.Button(
            self.frame_botones, 
            text="Registrar Salida", 
            command=self.registrar_salida
        )
        self.registrar_salida_button.grid(row=0, column=1, padx=5, pady=5)

        # Botón para generar reporte
        self.reporte_button = tk.Button(
            self.frame_botones, 
            text="Generar Reporte", 
            command=self.generar_reporte
        )
        self.reporte_button.grid(row=0, column=2, padx=5, pady=5)

    def registrar_entrada(self):
        """
        Registra la entrada de un vehículo en el parqueadero.
        """
        placa = self.placa_entry.get().strip()
        tipo = self.tipo_entry.get().strip().lower()

        # Validar entradas
        if not placa or not tipo:
            messagebox.showerror("Error", "Por favor, ingrese la placa y el tipo del vehículo.")
            return
        if tipo not in ["carro", "moto", "bicicleta"]:
            messagebox.showerror("Error", "Tipo de vehículo no válido. Use 'carro', 'moto' o 'bicicleta'.")
            return

        # Registrar el vehículo
        vehiculo = Vehiculo(placa, tipo)
        try:
            self.parqueadero.registrar_entrada(vehiculo)
            messagebox.showinfo("Éxito", f"Vehículo {placa} registrado con éxito.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def registrar_salida(self):
        """
        Registra la salida de un vehículo del parqueadero.
        """
        placa = self.placa_entry.get().strip()

        # Validar entrada
        if not placa:
            messagebox.showerror("Error", "Por favor, ingrese la placa del vehículo.")
            return

        # Registrar la salida
        try:
            costo = self.parqueadero.registrar_salida(placa)
            messagebox.showinfo("Éxito", f"Vehículo {placa} salió. Costo: ${costo:.2f}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def generar_reporte(self):
        """
        Genera y muestra un reporte del estado actual del parqueadero.
        """
        reporte = self.parqueadero.generar_reporte()

        # Formatear el reporte para mostrarlo en un messagebox
        reporte_formateado = (
            f"Espacios disponibles: {reporte['espacios_disponibles']}\n\n"
            f"Vehículos estacionados:\n"
        )

        for vehiculo_info in reporte["vehiculos_estacionados"]:
            reporte_formateado += f"- {vehiculo_info}\n"

        reporte_formateado += f"\nTotal recaudado: ${reporte['total_recaudado']:.2f}"

        # Mostrar el reporte en un messagebox
        messagebox.showinfo("Reporte", reporte_formateado)