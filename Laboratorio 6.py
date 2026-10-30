# URL del repositorio de GitHub: https://github.com/Fermin555/Laboratorio-6.git
# Autores: Fermin Delgado, Kevin Ulloa

import tkinter as tk
import numpy as np


# =========================================================================
# FUNCIONES MATEMÁTICAS (El "motor" del programa)
# =========================================================================

def eval_f(x):
    """Evalúa el polinomio de grado 6 en un punto x."""
    try:
        # Extraemos los números que el usuario escribió en las cajitas y los convertimos a float
        c = [float(e.get()) for e in entradas_coef]
        # Armamos el polinomio evaluado: a6*x^6 + a5*x^5 + ... + a0
        return c[0]*x**6 + c[1]*x**5 + c[2]*x**4 + c[3]*x**3 + c[4]*x**2 + c[5]*x + c[6]
    except ValueError:
        return 0

def eval_df(x):
    """Evalúa la derivada exacta (analítica) del polinomio en un punto x."""
    try:
        c = [float(e.get()) for e in entradas_coef]
        # Derivada a mano: bajamos el exponente multiplicando y le restamos 1 al grado
        return 6*c[0]*x**5 + 5*c[1]*x**4 + 4*c[2]*x**3 + 3*c[3]*x**2 + 2*c[4]*x + c[5]
    except ValueError:
        return 0


# =========================================================================
# LÓGICA: CÁLCULO DE RAÍCES
# =========================================================================

def calcular_raiz():
    try:
        # Leemos qué método eligió el usuario en los radiobuttons
        metodo = metodo_raiz.get()
        max_iter = int(entry_maxiter.get())
        
        # Determinamos cómo vamos a frenar el bucle (por error tolerado o por cifras significativas)
        if criterio_parada.get() == "Error":
            es = float(entry_es.get())
            cifras = 4 # Valor por defecto para el formato si solo nos dan el error
        else:
            cifras = int(entry_cifras.get())
            # Fórmula de Scarbourough para calcular el error tolerado en base a las cifras
            es = 0.5 * (10 ** (2 - cifras))
        
        # Habilitamos las casillas de resultado para poder limpiarlas y escribir
        for entry in [entry_raiz, entry_iter, entry_ea, entry_fraiz]:
            entry.config(state="normal")
            entry.delete(0, tk.END)

        xr = None
        ea = 100.0 # Error aproximado inicial gigante para que entre al bucle
        iters = 0

        # --- MÉTODO DE BISECCIÓN ---
        if metodo == "Biseccion":
            xl = float(entry_xi.get())
            xu = float(entry_xu.get())
            
            # Chequeamos el Teorema de Bolzano: si no hay cambio de signo, no hay raíz garantizada
            if eval_f(xl) * eval_f(xu) > 0:
                entry_raiz.insert(0, "Sin cambio de signo")
                return
                
            for i in range(max_iter):
                xrold = xr if xr is not None else xl
                xr = (xl + xu) / 2.0 # Partimos el intervalo a la mitad
                iters += 1
                
                # Calculamos el error relativo porcentual
                if xr != 0:
                    ea = abs((xr - xrold) / xr) * 100.0
                
                # Vemos de qué lado quedó la raíz para ajustar los límites
                test = eval_f(xl) * eval_f(xr)
                if test < 0:
                    xu = xr # La raíz está en la mitad izquierda
                elif test > 0:
                    xl = xr # La raíz está en la mitad derecha
                else:
                    ea = 0.0 # Le pegamos exacto a la raíz
                
                # Si alcanzamos la precisión deseada, cortamos el bucle
                if ea < es:
                    break

        # --- MÉTODO DE NEWTON-RAPHSON ---
        elif metodo == "Newton":
            xr = float(entry_xu.get()) # Tomamos el valor inicial
            for i in range(max_iter):
                xrold = xr
                d = eval_df(xr) # Calculamos la pendiente (derivada)
                
                # Si la pendiente es 0, la tangente es horizontal y no cruza el eje X. ¡Explota!
                if d == 0:
                    entry_raiz.insert(0, "Derivada nula")
                    return
                    
                # Fórmula iterativa de Newton
                xr = xr - eval_f(xr) / d
                iters += 1
                
                if xr != 0:
                    ea = abs((xr - xrold) / xr) * 100.0
                if ea < es:
                    break

        # --- MÉTODO DE LA SECANTE ---
        elif metodo == "Secante":
            x_1 = float(entry_xi.get()) # x_{i-1}
            x0 = float(entry_xu.get())  # x_i
            
            for i in range(max_iter):
                f0 = eval_f(x0)
                f1 = eval_f(x_1)
                
                # Evitamos división por cero si las alturas son iguales
                if f0 - f1 == 0:
                    entry_raiz.insert(0, "División por cero")
                    return
                    
                # Fórmula iterativa de la Secante (traza una recta entre dos puntos anteriores)
                xr = x0 - f0 * (x_1 - x0) / (f1 - f0)
                iters += 1
                
                if xr != 0:
                    ea = abs((xr - x0) / xr) * 100.0
                
                # Desplazamos los puntos para la próxima iteración
                x_1 = x0
                x0 = xr
                if ea < es:
                    break

        # --- MOSTRAR RESULTADOS DE RAÍCES ---
        if xr is not None:
            # Damos formato para mostrar solo la cantidad de cifras significativas pedidas
            fmt = f"{{:.{cifras}f}}"
            entry_raiz.insert(0, fmt.format(xr))
            entry_iter.insert(0, str(iters))
            entry_ea.insert(0, f"{ea:.4f}")
            entry_fraiz.insert(0, fmt.format(eval_f(xr)))

    except ValueError:
        entry_raiz.insert(0, "Error en datos")
    finally:
        # Volvemos a bloquear las casillas para que el usuario no las rompa
        for entry in [entry_raiz, entry_iter, entry_ea, entry_fraiz]:
            entry.config(state="readonly")


# =========================================================================
# LÓGICA: DERIVADA NUMÉRICA, GAUSS E INTEGRAL
# =========================================================================

def calcular_derivada():
    """Calcula la derivada primera usando el método de diferencia finita centrada."""
    try:
        x0 = float(entry_dx0.get())
        dx = float(entry_ddx.get())
        
        # Fórmula centrada: ( f(x+h) - f(x-h) ) / 2h
        # Es mucho más precisa que la hacia adelante o hacia atrás porque cancela errores de truncamiento.
        derivada = (eval_f(x0 + dx) - eval_f(x0 - dx)) / (2 * dx)
        
        entry_dres.config(state="normal")
        entry_dres.delete(0, tk.END)
        entry_dres.insert(0, f"{derivada:.4f}")
        entry_dres.config(state="readonly")
    except ValueError:
        entry_dres.config(state="normal")
        entry_dres.delete(0, tk.END)
        entry_dres.insert(0, "Error")
        entry_dres.config(state="readonly")

def calcular_gauss():
    """Resuelve el sistema de ecuaciones 4x4 mediante Eliminación Gaussiana."""
    try:
        N = 4
        # Preparamos matrices vacías llenas de ceros en Numpy
        A = np.zeros((N, N))
        b = np.zeros(N)
        
        # Llenamos las matrices con lo que el usuario tipeó
        for i in range(N):
            for j in range(N):
                A[i][j] = float(entradas_gauss_A[i][j].get())
            b[i] = float(entradas_gauss_b[i].get())
            
        pivoteo = opcion_pivoteo.get()
        
        for entry in entradas_gauss_res:
            entry.config(state="normal")
            entry.delete(0, tk.END)

        # Fase de Eliminación Hacia Adelante
        for q in range(N-1):
            # Si el usuario tildó Pivoteo Parcial, buscamos el valor más grande en la columna
            if pivoteo == 1:
                p = q
                for i in range(q+1, N):
                    if abs(A[i][q]) > abs(A[p][q]):
                        p = i
                # Intercambiamos filas en A y en b para poner el mayor arriba (evita división por cero y reduce errores)
                A[[q, p]] = A[[p, q]]
                b[[q, p]] = b[[p, q]]
            
            # Si el pivote quedó en cero (o casi cero), el sistema no tiene solución única
            if abs(A[q][q]) < 1e-12:
                entradas_gauss_res[0].insert(0, "Pivote nulo")
                for entry in entradas_gauss_res:
                    entry.config(state="readonly")
                return
            
            # Triangularizamos: hacemos ceros por debajo del pivote
            for k in range(q+1, N):
                m = A[k][q] / A[q][q] # Multiplicador
                A[k] = A[k] - m * A[q]
                b[k] = b[k] - m * b[q]
                
        # Chequeo final del último pivote de la diagonal
        if abs(A[N-1][N-1]) < 1e-12:
            entradas_gauss_res[0].insert(0, "Pivote nulo")
            for entry in entradas_gauss_res:
                entry.config(state="readonly")
            return

        # Fase de Sustitución Hacia Atrás (despejamos desde x4 hasta x1)
        x = np.zeros(N)
        for i in range(N-1, -1, -1):
            s = sum(A[i][j] * x[j] for j in range(i+1, N))
            x[i] = (b[i] - s) / A[i][i]
            
        # Mostramos resultados
        for i in range(N):
            entradas_gauss_res[i].insert(0, f"{x[i]:.4f}")
            
    except ValueError:
        entradas_gauss_res[0].config(state="normal")
        entradas_gauss_res[0].insert(0, "Error")
    finally:
        for entry in entradas_gauss_res:
            entry.config(state="readonly")

def borrar_gauss():
    """Limpia todos los campos de la matriz de Gauss."""
    for i in range(4):
        for j in range(4):
            entradas_gauss_A[i][j].delete(0, tk.END)
        entradas_gauss_b[i].delete(0, tk.END)
        entradas_gauss_res[i].config(state="normal")
        entradas_gauss_res[i].delete(0, tk.END)
        entradas_gauss_res[i].config(state="readonly")

def valores_prueba_gauss():
    """Carga rápidamente los datos de prueba del TP para no tener que tipear todo a mano."""
    borrar_gauss()
    val_A = [["2", "2", "1", "-1"], ["2", "-2", "6", "-4"], ["2", "2", "1", "1"], ["1", "5", "-4", "-2"]]
    val_b = ["5", "0", "13", "-9"]
    for i in range(4):
        for j in range(4):
            entradas_gauss_A[i][j].insert(0, val_A[i][j])
        entradas_gauss_b[i].insert(0, val_b[i])

def calcular_integral():
    """Calcula el área bajo la curva usando Regla de Simpson 1/3 Compuesta."""
    try:
        a = float(entry_inta.get())
        b = float(entry_intb.get())
        n = int(entry_intn.get())
        
        entry_intres.config(state="normal")
        entry_intres.delete(0, tk.END)
        
        # Condición matemática estricta: Simpson 1/3 agrupa de a pares, así que 'n' debe ser par.
        if n % 2 != 0 or n <= 0:
            entry_intres.insert(0, "n debe ser par")
            entry_intres.config(state="readonly")
            return
            
        h = (b - a) / n # Tamaño de paso
        suma = eval_f(a) + eval_f(b) # Los extremos se suman normales
        
        # Iteramos los puntos intermedios: los impares se multiplican por 4 y los pares por 2
        for i in range(1, n):
            x = a + i * h
            if i % 2 == 0:
                suma += 2 * eval_f(x)
            else:
                suma += 4 * eval_f(x)
                
        # Multiplicamos por la base de la parábola
        integral = (h / 3) * suma
        
        entry_intres.insert(0, f"{integral:.4f}")
    except ValueError:
        entry_intres.config(state="normal")
        entry_intres.insert(0, "Error")
    finally:
        entry_intres.config(state="readonly")


# =========================================================================
# INTERFAZ GRÁFICA (GUI) - Estructura visual
# =========================================================================

# Creamos la ventana principal, el lienzo donde vamos a dibujar todo
ventana = tk.Tk()
ventana.title("Laboratorio VI.1 - Cálculo Numérico")
ventana.geometry("850x650")


# =========================================================================
# PASO 1: Coeficientes del polinomio
# =========================================================================
frame_poli = tk.Frame(ventana, padx=10, pady=10)
frame_poli.pack(fill="x") # pack() acomoda el panel ocupando todo el ancho de arriba

tk.Label(frame_poli, text="Coeficientes\ndel polinomio", font=("Arial", 9, "bold")).grid(row=0, column=0, rowspan=2, padx=10)
entradas_coef = []
textos_labels = ["a6", "a5", "a4", "a3", "a2", "a1", "a0"]

# Valores por defecto para testear rápido
valores_prueba = ["0", "1", "0", "-8", "0", "82", "-25"] 

# Armamos las 7 casillas de los coeficientes con un bucle
for i in range(7):
    entry = tk.Entry(frame_poli, width=7, justify="center")
    entry.insert(0, valores_prueba[i])
    entry.grid(row=0, column=i+1, padx=5)
    entradas_coef.append(entry)
    tk.Label(frame_poli, text=textos_labels[i]).grid(row=1, column=i+1)

tk.Button(frame_poli, text="Borrar").grid(row=0, column=8, padx=20, sticky="we")
tk.Button(frame_poli, text="Valores de prueba").grid(row=1, column=8, padx=20, sticky="we")


# =========================================================================
# PASO 2: Cálculo de una raíz
# =========================================================================
frame_raices = tk.LabelFrame(ventana, text="Cálculo de una raíz", padx=10, pady=10)
frame_raices.pack(fill="x", padx=10, pady=5)

metodo_raiz = tk.StringVar(value="Biseccion")
criterio_parada = tk.StringVar(value="Error")

# Botones de radio para elegir qué método matemático usar
tk.Label(frame_raices, text="Método:").grid(row=0, column=0, sticky="e")
tk.Radiobutton(frame_raices, text="Bisección", variable=metodo_raiz, value="Biseccion").grid(row=0, column=1)
tk.Radiobutton(frame_raices, text="Newton-Raphson", variable=metodo_raiz, value="Newton").grid(row=0, column=2)
tk.Radiobutton(frame_raices, text="Secante", variable=metodo_raiz, value="Secante").grid(row=0, column=3)

# Casilla bloqueada (readonly) donde escupimos la raíz encontrada
tk.Label(frame_raices, text="Raíz:").grid(row=0, column=5, sticky="e", padx=(40,5))
entry_raiz = tk.Entry(frame_raices, width=15, state="readonly")
entry_raiz.grid(row=0, column=6)

# Puntos iniciales dependiendo del método
tk.Label(frame_raices, text="xl / x0 / x-1:").grid(row=1, column=0, sticky="e", pady=5)
entry_xi = tk.Entry(frame_raices, width=8)
entry_xi.insert(0, "0")
entry_xi.grid(row=1, column=1, sticky="w")

tk.Label(frame_raices, text="xu / x0:").grid(row=1, column=2, sticky="e")
entry_xu = tk.Entry(frame_raices, width=8)
entry_xu.insert(0, "1")
entry_xu.grid(row=1, column=3, sticky="w")

# BOTÓN MAGICO DE CÁLCULO que llama a la función
tk.Button(frame_raices, text="Calcular", command=calcular_raiz).grid(row=1, column=4, padx=15, rowspan=2)

tk.Label(frame_raices, text="Iteraciones:").grid(row=1, column=5, sticky="e", padx=(40,5))
entry_iter = tk.Entry(frame_raices, width=15, state="readonly")
entry_iter.grid(row=1, column=6)

# Frame interno para amontonar los criterios de parada
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

# Casillas para los resultados de error y función evaluada
tk.Label(frame_raices, text="εa (%):").grid(row=2, column=5, sticky="e", padx=(40,5))
entry_ea = tk.Entry(frame_raices, width=15, state="readonly")
entry_ea.grid(row=2, column=6)

tk.Label(frame_raices, text="f(raíz):").grid(row=3, column=5, sticky="e", padx=(40,5))
entry_fraiz = tk.Entry(frame_raices, width=15, state="readonly")
entry_fraiz.grid(row=3, column=6)


# =========================================================================
# PASO 3: Cálculo de la derivada primera
# =========================================================================
frame_derivada = tk.LabelFrame(ventana, text="Cálculo de la derivada primera (diferencia centrada)", padx=10, pady=10)
frame_derivada.pack(fill="x", padx=10, pady=5)

tk.Label(frame_derivada, text="x0:").grid(row=0, column=0, sticky="e")
entry_dx0 = tk.Entry(frame_derivada, width=10)
entry_dx0.insert(0, "1")
entry_dx0.grid(row=0, column=1, padx=5)

tk.Label(frame_derivada, text="dx:").grid(row=0, column=2, sticky="e")
entry_ddx = tk.Entry(frame_derivada, width=10)
entry_ddx.insert(0, "0.1")
entry_ddx.grid(row=0, column=3, padx=5)

tk.Button(frame_derivada, text="Calcular", command=calcular_derivada).grid(row=0, column=4, padx=20)

tk.Label(frame_derivada, text="Derivada f'(x0):").grid(row=0, column=5, sticky="e", padx=(40,5))
entry_dres = tk.Entry(frame_derivada, width=15, state="readonly")
entry_dres.grid(row=0, column=6)


# =========================================================================
# PASO 3.1: Resolución de sistema (Eliminación de Gauss)
# =========================================================================
frame_gauss = tk.LabelFrame(ventana, text="Resolución de un sistema de 4 ecuaciones (eliminación gaussiana)", padx=10, pady=10)
frame_gauss.pack(fill="x", padx=10, pady=5)

for j in range(4):
    tk.Label(frame_gauss, text=f"x{j+1}").grid(row=0, column=j)
tk.Label(frame_gauss, text="b").grid(row=0, column=4, padx=(10,0))

entradas_gauss_A = []
entradas_gauss_b = []
entradas_gauss_res = []

# Carga dura de los valores de prueba
val_A = [["2", "2", "1", "-1"],
         ["2", "-2", "6", "-4"],
         ["2", "2", "1", "1"],
         ["1", "5", "-4", "-2"]]
val_b = ["5", "0", "13", "-9"]

# Generamos la cuadrícula 4x4 visual en la interfaz usando un doble bucle iterativo
for i in range(4):
    fila = []
    for j in range(4):
        ent = tk.Entry(frame_gauss, width=8, justify="center")
        ent.insert(0, val_A[i][j])
        ent.grid(row=i+1, column=j, padx=2, pady=2)
        fila.append(ent)
    entradas_gauss_A.append(fila)
    
    # Columna independiente b
    ent_b = tk.Entry(frame_gauss, width=8, justify="center")
    ent_b.insert(0, val_b[i])
    ent_b.grid(row=i+1, column=4, padx=(15,5), pady=2)
    entradas_gauss_b.append(ent_b)

# Panelcito lateral para decidir si usamos o no pivoteo
frame_opc_gauss = tk.Frame(frame_gauss)
frame_opc_gauss.grid(row=1, column=5, rowspan=4, padx=20)

opcion_pivoteo = tk.IntVar(value=0)
tk.Radiobutton(frame_opc_gauss, text="Sin pivoteo", variable=opcion_pivoteo, value=0).pack(anchor="w")
tk.Radiobutton(frame_opc_gauss, text="Con pivoteo parcial", variable=opcion_pivoteo, value=1).pack(anchor="w")

tk.Button(frame_opc_gauss, text="Calcular", command=calcular_gauss).pack(fill="x", pady=(5,2))
tk.Button(frame_opc_gauss, text="Borrar", command=borrar_gauss).pack(fill="x", pady=2)
tk.Button(frame_opc_gauss, text="Valores de prueba", command=valores_prueba_gauss).pack(fill="x", pady=2)

# Panel para mostrar el despeje de las 4 X
frame_res_gauss = tk.Frame(frame_gauss)
frame_res_gauss.grid(row=1, column=6, rowspan=4, padx=10)

for i in range(4):
    tk.Label(frame_res_gauss, text=f"x{i+1} =").grid(row=i, column=0, sticky="e")
    ent_res = tk.Entry(frame_res_gauss, width=12, state="readonly")
    ent_res.grid(row=i, column=1, pady=2, padx=5)
    entradas_gauss_res.append(ent_res)


# =========================================================================
# PASO 4: Cálculo de la integral definida
# =========================================================================
frame_integral = tk.LabelFrame(ventana, text="Cálculo de la integral definida (Simpson 1/3 compuesta)", padx=10, pady=10)
frame_integral.pack(fill="x", padx=10, pady=5)

tk.Label(frame_integral, text="Intervalo de integración:   a:").grid(row=0, column=0, sticky="e")
entry_inta = tk.Entry(frame_integral, width=8)
entry_inta.insert(0, "0")
entry_inta.grid(row=0, column=1, padx=5)

tk.Label(frame_integral, text="b:").grid(row=0, column=2, sticky="e")
entry_intb = tk.Entry(frame_integral, width=8)
entry_intb.insert(0, "2")
entry_intb.grid(row=0, column=3, padx=5, sticky="w")

tk.Button(frame_integral, text="Calcular", command=calcular_integral).grid(row=0, column=4, rowspan=2, padx=40)

tk.Label(frame_integral, text="Integral definida:").grid(row=0, column=5, rowspan=2, sticky="e", padx=(10,5))
entry_intres = tk.Entry(frame_integral, width=15, state="readonly")
entry_intres.grid(row=0, column=6, rowspan=2)

tk.Label(frame_integral, text="Cantidad de subintervalos (par):").grid(row=1, column=0, columnspan=2, sticky="e", pady=10)
entry_intn = tk.Entry(frame_integral, width=8)
entry_intn.insert(0, "2")
entry_intn.grid(row=1, column=2, columnspan=2, sticky="w", padx=5)


# =========================================================================
# INICIO DE LA APLICACIÓN
# =========================================================================
# El bucle infinito que mantiene la ventana abierta y "escuchando"
ventana.mainloop()