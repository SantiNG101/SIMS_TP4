import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from utils import analytic_solution

def compute_ecm(num, ana):
    return np.mean((num - ana)**2)

def plot(filename):
    out_folder = "outputs/oscillator"
    sims_folder = out_folder + "/sim_results"

    fn = os.path.join(sims_folder, filename + "_out.csv")
    out = os.path.join(out_folder, filename + "_oscillator.png")

    # parámetros del problema (de Main.java)
    m = 70.0
    k = 1e4
    gamma = 100.0
    A = 1.0

    # cargar datos numéricos
    data = np.loadtxt(fn, delimiter=",", skiprows=1)
    t = data[:,0]
    x_num = data[:,2]  # columna x
    v_num = data[:,5]  # columna vx

    # solución analítica
    x_ana, v_ana = analytic_solution(t, A, m, k, gamma)

    # calcular errores
    ecm_x = compute_ecm(x_num, x_ana)
    ecm_v = compute_ecm(v_num, v_ana)
    print(f"ECM posición = {ecm_x:.3e}")
    print(f"ECM velocidad = {ecm_v:.3e}")

    # graficar
    plt.figure(figsize=(8,5))
    plt.plot(t, x_num, label="x numérico", alpha=0.7)
    plt.plot(t, x_ana, "--", label="x analítico")
    plt.xlabel("Tiempo")
    plt.ylabel("x(t)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out, dpi=150)


if __name__ == "__main__":

    integrators = ["verlet", "beeman"]   # "verlet", "beeman", "gear5"
    dts = ["0.01", "0.001", "1.0E-4"]

    for integrator in integrators:
        for d in dts:
            filename = integrator + "_" + d
            plot(filename)
