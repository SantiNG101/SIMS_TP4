import numpy as np
import matplotlib.pyplot as plt
import os
from utils import analytic_solution

def compute_ecm(integrators, dts):
    ecm_dict = {integr: [] for integr in integrators}

    out_folder = "outputs/oscillator"
    sims_folder = out_folder + "/sim_results"

    for integr in integrators:
        for dt in dts:
            fn = f"{integr}_{dt}_out.csv"
            filename = os.path.join(sims_folder, fn)
            data = np.genfromtxt(filename, delimiter=",", skip_header=1)  # saltamos la cabecera
            t = data[:,0]  # columna time
            x_num = data[:,2]  # columna x
            x_ana, _ = analytic_solution(t)  # calculamos analítica
            ecm = np.mean((x_num - x_ana)**2)  # error cuadrático medio
            ecm_dict[integr].append(ecm)
    return integrators, dts, ecm_dict


# Graficar ECM vs dt en escala log-log
def plot(integrators, dts, ecm_dict, fontsize):
    dts_float = [float(dt) for dt in dts]
    out_folder = "outputs/oscillator"

    plt.figure(figsize=(7,5))
    for integr in integrators:
        plt.loglog(dts_float, ecm_dict[integr], marker='o', label=integr)

    plt.xlabel('dt (s)', fontsize=fontsize)
    plt.ylabel('Error cuadrático medio (ECM)', fontsize=fontsize)
    plt.grid(True, which="both", ls="--")
    plt.legend(fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.savefig(os.path.join(out_folder, "ecm_vs_dt.png"), dpi=150)



if __name__ == "__main__":
    integrators = ["gear5", "beeman", "verlet"]
    dts = ["0.01", "0.001", "1.0E-4", "1.0E-5"]
    fontsize = 14

    integrators, dts, ecm_dict = compute_ecm(integrators, dts)
    plot(integrators, dts, ecm_dict, fontsize)