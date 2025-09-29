import numpy as np
import os
import matplotlib.pyplot as plt
from utils import analytic_solution

def plot(dt):

    out_folder = "outputs/oscillator"
    sims_folder = out_folder + "/sim_results"

    out = os.path.join(out_folder, "compare_integrators_zoom.png")

    # archivos de salida de cada integrador (ajustá rutas si hace falta)
    files = {
        "Gear5": os.path.join(sims_folder, f"gear5_{dt}_out.csv"),
        "Beeman": os.path.join(sims_folder, f"beeman_{dt}_out.csv"),
        "Verlet": os.path.join(sims_folder, f"verlet_{dt}_out.csv"),
    }

    # rangos de tiempo que querés visualizar
    t_min = 1.0000
    t_max = 1.0002

    data = {}
    for name, fn in files.items():
        arr = np.loadtxt(fn, delimiter=",", skiprows=1)
        t = arr[:,0]
        x = arr[:,2]
        # aplicar filtro por rango
        mask = (t >= t_min) & (t <= t_max)
        data[name] = (t[mask], x[mask])

    # curva analítica en el mismo rango
    t_ref = np.linspace(t_min, t_max, 500)
    x_ana_curve, v = analytic_solution(t_ref)

    # graficar
    plt.figure(figsize=(8,5))
    plt.plot(t_ref, x_ana_curve, 'k--', label='Analítico')

    for name,(t,x) in data.items():
        plt.plot(t, x, label=name)

    plt.xlabel("Tiempo [s]")
    plt.ylabel("x(t)")
    plt.title(f"Comparación integradores ({t_min:.2f} ≤ t ≤ {t_max:.2f})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out, dpi=150)


if __name__ == "__main__":
    dt = "1.0E-4"  # elegir paso temporal
    plot(dt)
