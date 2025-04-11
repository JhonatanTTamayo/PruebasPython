# main.py
import tkinter as tk
from parqueadero.interfaz import InterfazParqueadero

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazParqueadero(root)
    root.mainloop()