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

# --- PASO 2: Cálculo de una raíz ---
# Usamos LabelFrame para que tenga el borde y el título agrupador
frame_raices = tk.LabelFrame(ventana, text="Cálculo de una raíz", padx=10, pady=10)
frame_raices.pack(fill="x", padx=10, pady=5)

# Variables de control para las opciones seleccionables (Radiobuttons)
metodo_raiz = tk.StringVar(value="Biseccion")
criterio_parada = tk.StringVar(value="Error")

# Fila 0: Selección de método y resultado Raíz
tk.Label(frame_raices, text="Método:").grid(row=0, column=0, sticky="e")
tk.Radiobutton(frame_raices, text="Bisección", variable=metodo_raiz, value="Biseccion").grid(row=0, column=1)
tk.Radiobutton(frame_raices, text="Newton-Raphson", variable=metodo_raiz, value="Newton").grid(row=0, column=2)
tk.Radiobutton(frame_raices, text="Secante", variable=metodo_raiz, value="Secante").grid(row=0, column=3)

tk.Label(frame_raices, text="Raíz:").grid(row=0, column=5, sticky="e", padx=(40,5))
entry_raiz = tk.Entry(frame_raices, width=15, state="readonly")
entry_raiz.grid(row=0, column=6)

# Fila 1: Valores iniciales y resultado Iteraciones
tk.Label(frame_raices, text="xl / x0 / x-1:").grid(row=1, column=0, sticky="e", pady=5)
entry_xi = tk.Entry(frame_raices, width=8)
entry_xi.insert(0, "0")
entry_xi.grid(row=1, column=1, sticky="w")

tk.Label(frame_raices, text="xu / x0:").grid(row=1, column=2, sticky="e")
entry_xu = tk.Entry(frame_raices, width=8)
entry_xu.insert(0, "1")
entry_xu.grid(row=1, column=3, sticky="w")

# Botón central (sin funcionalidad por ahora)
tk.Button(frame_raices, text="Calcular").grid(row=1, column=4, padx=15, rowspan=2)

tk.Label(frame_raices, text="Iteraciones:").grid(row=1, column=5, sticky="e", padx=(40,5))
entry_iter = tk.Entry(frame_raices, width=15, state="readonly")
entry_iter.grid(row=1, column=6)

# Fila 2 y 3: Criterios de parada y resultados de error/función
frame_criterios = tk.Frame(frame_raices)
frame_criterios.grid(row=2, column=0, columnspan=4, pady=5)

tk.Radiobutton(frame_criterios, text="εs (%):", variable=criterio_parada, value="Error").pack(side="left")
entry_es = tk.Entry(frame_criterios, width=6)
entry_es.insert(0, "0.5")
entry_es.pack(side="left", padx=5)

tk.Radiobutton(frame_criterios, text="Cifras signif.:", variable=criterio_parada, value="Cifras").pack(side="left")
entry_cifras = tk.Entry(frame_criterios, width=6)
entry_cifras.insert(0, "4")
entry_cifras.pack(side="left", padx=5)

tk.Label(frame_criterios, text="Máx. iter.:").pack(side="left", padx=(10,2))
entry_maxiter = tk.Entry(frame_criterios, width=6)
entry_maxiter.insert(0, "100")
entry_maxiter.pack(side="left")

tk.Label(frame_raices, text="εa (%):").grid(row=2, column=5, sticky="e", padx=(40,5))
entry_ea = tk.Entry(frame_raices, width=15, state="readonly")
entry_ea.grid(row=2, column=6)

tk.Label(frame_raices, text="f(raíz):").grid(row=3, column=5, sticky="e", padx=(40,5))
entry_fraiz = tk.Entry(frame_raices, width=15, state="readonly")
entry_fraiz.grid(row=3, column=6)

# Iniciar el bucle de eventos para mantener la ventana abierta
ventana.mainloop()