import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def analytic_solution(t, A, m, k, gamma):
    w0 = np.sqrt(k/m)
    beta = gamma/(2*m)
    wd = np.sqrt(w0**2 - beta**2)
    x = A * np.exp(-beta*t) * np.cos(wd*t)
    v = -A * np.exp(-beta*t) * (beta*np.cos(wd*t) + wd*np.sin(wd*t))
    return x, v

def compute_ecm(num, ana):
    return np.mean((num - ana)**2)

def plot(integratorName):
    out_folder = "outputs/oscillator"
    sims_folder = out_folder + "/sim_results"

    fn = os.path.join(sims_folder, integratorName + "_out.csv")
    out = os.path.join(out_folder, integratorName + "_oscillator.png")

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
    plt.show()


if __name__ == "__main__":
    
    integratorName = "verlet" # "verlet", "beeman", "gear5"

    plot(integratorName)
