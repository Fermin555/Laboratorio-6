# URL del repositorio de GitHub: https://github.com/Fermin555/Laboratorio-6.git
# Autores: Fermin Delgado, Kevin Ulloa

import tkinter as tk
import numpy as np

# --- Configuración de la ventana principal ---
ventana = tk.Tk()
ventana.title("Laboratorio VI.1 - Cálculo Numérico")
ventana.geometry("850x650") # Tamaño inicial de la ventana

# --- PASO 1: Coeficientes del polinomio ---
frame_poli = tk.Frame(ventana, padx=10, pady=10)
frame_poli.pack(fill="x")

# Etiqueta principal
tk.Label(frame_poli, text="Coeficientes\ndel polinomio", font=("Arial", 9, "bold")).grid(row=0, column=0, rowspan=2, padx=10)

# Listas para guardar las cajas de texto y configurarlas
entradas_coef = []
textos_labels = ["a6", "a5", "a4", "a3", "a2", "a1", "a0"]
# Valores predeterminados de la consigna: f(x) = x^5 - 8x^3 + 82x - 25
valores_prueba = ["0", "1", "0", "-8", "0", "82", "-25"] 

for i in range(7):
    # Caja de texto para el coeficiente
    entry = tk.Entry(frame_poli, width=7, justify="center")
    entry.insert(0, valores_prueba[i]) # Insertamos el valor por defecto
    entry.grid(row=0, column=i+1, padx=5)
    entradas_coef.append(entry)
    
    # Etiqueta debajo de la caja (a6 ... a0)
    tk.Label(frame_poli, text=textos_labels[i]).grid(row=1, column=i+1)

# Botones laterales (por ahora solo visuales, les daremos vida más adelante)
tk.Button(frame_poli, text="Borrar").grid(row=0, column=8, padx=20, sticky="we")
tk.Button(frame_poli, text="Valores de prueba").grid(row=1, column=8, padx=20, sticky="we")

# Iniciar el bucle de eventos para mantener la ventana abierta
ventana.mainloop()