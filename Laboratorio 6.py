# URL del repositorio de GitHub: https://github.com/Fermin555/Laboratorio-6.git
# Autores: Fermin Delgado, Kevin Ulloa

# URL del repositorio de GitHub: [ACÁ VA EL LINK A TU REPO]
import tkinter as tk
import numpy as np

# =========================================================================
# FUNCIONES MATEMÁTICAS (Tienen que ir arriba para que los botones las vean)
# =========================================================================
def eval_f(x):
    try:
        c = [float(e.get()) for e in entradas_coef]
        return c[0]*x**6 + c[1]*x**5 + c[2]*x**4 + c[3]*x**3 + c[4]*x**2 + c[5]*x + c[6]
    except ValueError:
        return 0

def eval_df(x):
    try:
        c = [float(e.get()) for e in entradas_coef]
        return 6*c[0]*x**5 + 5*c[1]*x**4 + 4*c[2]*x**3 + 3*c[3]*x**2 + 2*c[4]*x + c[5]
    except ValueError:
        return 0

def calcular_raiz():
    try:
        metodo = metodo_raiz.get()
        max_iter = int(entry_maxiter.get())
        
        if criterio_parada.get() == "Error":
            es = float(entry_es.get())
            cifras = 4 
        else:
            cifras = int(entry_cifras.get())
            es = 0.5 * (10 ** (2 - cifras))
        
        for entry in [entry_raiz, entry_iter, entry_ea, entry_fraiz]:
            entry.config(state="normal")
            entry.delete(0, tk.END)

        xr = None
        ea = 100.0
        iters = 0

        if metodo == "Biseccion":
            xl = float(entry_xi.get())
            xu = float(entry_xu.get())
            
            if eval_f(xl) * eval_f(xu) > 0:
                entry_raiz.insert(0, "Sin cambio de signo")
                return
                
            for i in range(max_iter):
                xrold = xr if xr is not None else xl
                xr = (xl + xu) / 2.0
                iters += 1
                if xr != 0:
                    ea = abs((xr - xrold) / xr) * 100.0
                
                test = eval_f(xl) * eval_f(xr)
                if test < 0:
                    xu = xr
                elif test > 0:
                    xl = xr
                else:
                    ea = 0.0
                
                if ea < es:
                    break

        elif metodo == "Newton":
            xr = float(entry_xu.get())
            for i in range(max_iter):
                xrold = xr
                d = eval_df(xr)
                if d == 0:
                    entry_raiz.insert(0, "Derivada nula")
                    return
                xr = xr - eval_f(xr) / d
                iters += 1
                if xr != 0:
                    ea = abs((xr - xrold) / xr) * 100.0
                if ea < es:
                    break

        elif metodo == "Secante":
            x_1 = float(entry_xi.get())
            x0 = float(entry_xu.get())
            for i in range(max_iter):
                f0 = eval_f(x0)
                f1 = eval_f(x_1)
                if f0 - f1 == 0:
                    entry_raiz.insert(0, "División por cero")
                    return
                xr = x0 - f0 * (x_1 - x0) / (f1 - f0)
                iters += 1
                if xr != 0:
                    ea = abs((xr - x0) / xr) * 100.0
                x_1 = x0
                x0 = xr
                if ea < es:
                    break

        if xr is not None:
            fmt = f"{{:.{cifras}f}}"
            entry_raiz.insert(0, fmt.format(xr))
            entry_iter.insert(0, str(iters))
            entry_ea.insert(0, f"{ea:.4f}")
            entry_fraiz.insert(0, fmt.format(eval_f(xr)))

    except ValueError:
        entry_raiz.insert(0, "Error en datos")
    finally:
        for entry in [entry_raiz, entry_iter, entry_ea, entry_fraiz]:
            entry.config(state="readonly")

def calcular_derivada():
    try:
        x0 = float(entry_dx0.get())
        dx = float(entry_ddx.get())
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


# =========================================================================
# INTERFAZ GRÁFICA (GUI)
# =========================================================================
ventana = tk.Tk()
ventana.title("Laboratorio VI.1 - Cálculo Numérico")
ventana.geometry("850x650")

# --- PASO 1: Coeficientes del polinomio ---
frame_poli = tk.Frame(ventana, padx=10, pady=10)
frame_poli.pack(fill="x")

tk.Label(frame_poli, text="Coeficientes\ndel polinomio", font=("Arial", 9, "bold")).grid(row=0, column=0, rowspan=2, padx=10)
entradas_coef = []
textos_labels = ["a6", "a5", "a4", "a3", "a2", "a1", "a0"]
valores_prueba = ["0", "1", "0", "-8", "0", "82", "-25"] 

for i in range(7):
    entry = tk.Entry(frame_poli, width=7, justify="center")
    entry.insert(0, valores_prueba[i])
    entry.grid(row=0, column=i+1, padx=5)
    entradas_coef.append(entry)
    tk.Label(frame_poli, text=textos_labels[i]).grid(row=1, column=i+1)

tk.Button(frame_poli, text="Borrar").grid(row=0, column=8, padx=20, sticky="we")
tk.Button(frame_poli, text="Valores de prueba").grid(row=1, column=8, padx=20, sticky="we")

# --- PASO 2: Cálculo de una raíz ---
frame_raices = tk.LabelFrame(ventana, text="Cálculo de una raíz", padx=10, pady=10)
frame_raices.pack(fill="x", padx=10, pady=5)

metodo_raiz = tk.StringVar(value="Biseccion")
criterio_parada = tk.StringVar(value="Error")

tk.Label(frame_raices, text="Método:").grid(row=0, column=0, sticky="e")
tk.Radiobutton(frame_raices, text="Bisección", variable=metodo_raiz, value="Biseccion").grid(row=0, column=1)
tk.Radiobutton(frame_raices, text="Newton-Raphson", variable=metodo_raiz, value="Newton").grid(row=0, column=2)
tk.Radiobutton(frame_raices, text="Secante", variable=metodo_raiz, value="Secante").grid(row=0, column=3)

tk.Label(frame_raices, text="Raíz:").grid(row=0, column=5, sticky="e", padx=(40,5))
entry_raiz = tk.Entry(frame_raices, width=15, state="readonly")
entry_raiz.grid(row=0, column=6)

tk.Label(frame_raices, text="xl / x0 / x-1:").grid(row=1, column=0, sticky="e", pady=5)
entry_xi = tk.Entry(frame_raices, width=8)
entry_xi.insert(0, "0")
entry_xi.grid(row=1, column=1, sticky="w")

tk.Label(frame_raices, text="xu / x0:").grid(row=1, column=2, sticky="e")
entry_xu = tk.Entry(frame_raices, width=8)
entry_xu.insert(0, "1")
entry_xu.grid(row=1, column=3, sticky="w")

tk.Button(frame_raices, text="Calcular", command=calcular_raiz).grid(row=1, column=4, padx=15, rowspan=2)

tk.Label(frame_raices, text="Iteraciones:").grid(row=1, column=5, sticky="e", padx=(40,5))
entry_iter = tk.Entry(frame_raices, width=15, state="readonly")
entry_iter.grid(row=1, column=6)

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

# --- PASO 3: Cálculo de la derivada primera ---
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

# --- PASO 3.1: Resolución de sistema (Eliminación de Gauss) ---
frame_gauss = tk.LabelFrame(ventana, text="Resolución de un sistema de 4 ecuaciones (eliminación gaussiana)", padx=10, pady=10)
frame_gauss.pack(fill="x", padx=10, pady=5)

for j in range(4):
    tk.Label(frame_gauss, text=f"x{j+1}").grid(row=0, column=j)
tk.Label(frame_gauss, text="b").grid(row=0, column=4, padx=(10,0))

entradas_gauss_A = []
entradas_gauss_b = []
entradas_gauss_res = []

val_A = [["2", "2", "1", "-1"],
         ["2", "-2", "6", "-4"],
         ["2", "2", "1", "1"],
         ["1", "5", "-4", "-2"]]
val_b = ["5", "0", "13", "-9"]

for i in range(4):
    fila = []
    for j in range(4):
        ent = tk.Entry(frame_gauss, width=8, justify="center")
        ent.insert(0, val_A[i][j])
        ent.grid(row=i+1, column=j, padx=2, pady=2)
        fila.append(ent)
    entradas_gauss_A.append(fila)
    
    ent_b = tk.Entry(frame_gauss, width=8, justify="center")
    ent_b.insert(0, val_b[i])
    ent_b.grid(row=i+1, column=4, padx=(15,5), pady=2)
    entradas_gauss_b.append(ent_b)

frame_opc_gauss = tk.Frame(frame_gauss)
frame_opc_gauss.grid(row=1, column=5, rowspan=4, padx=20)

opcion_pivoteo = tk.IntVar(value=0)
tk.Radiobutton(frame_opc_gauss, text="Sin pivoteo", variable=opcion_pivoteo, value=0).pack(anchor="w")
tk.Radiobutton(frame_opc_gauss, text="Con pivoteo parcial", variable=opcion_pivoteo, value=1).pack(anchor="w")

tk.Button(frame_opc_gauss, text="Calcular").pack(fill="x", pady=(5,2))
tk.Button(frame_opc_gauss, text="Borrar").pack(fill="x", pady=2)
tk.Button(frame_opc_gauss, text="Valores de prueba").pack(fill="x", pady=2)

frame_res_gauss = tk.Frame(frame_gauss)
frame_res_gauss.grid(row=1, column=6, rowspan=4, padx=10)

for i in range(4):
    tk.Label(frame_res_gauss, text=f"x{i+1} =").grid(row=i, column=0, sticky="e")
    ent_res = tk.Entry(frame_res_gauss, width=12, state="readonly")
    ent_res.grid(row=i, column=1, pady=2, padx=5)
    entradas_gauss_res.append(ent_res)

# --- PASO 4: Cálculo de la integral definida ---
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

tk.Button(frame_integral, text="Calcular").grid(row=0, column=4, rowspan=2, padx=40)

tk.Label(frame_integral, text="Integral definida:").grid(row=0, column=5, rowspan=2, sticky="e", padx=(10,5))
entry_intres = tk.Entry(frame_integral, width=15, state="readonly")
entry_intres.grid(row=0, column=6, rowspan=2)

tk.Label(frame_integral, text="Cantidad de subintervalos (par):").grid(row=1, column=0, columnspan=2, sticky="e", pady=10)
entry_intn = tk.Entry(frame_integral, width=8)
entry_intn.insert(0, "2")
entry_intn.grid(row=1, column=2, columnspan=2, sticky="w", padx=5)

# =========================================================================
ventana.mainloop()