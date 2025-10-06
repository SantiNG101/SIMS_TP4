import numpy as np
import matplotlib.pyplot as plt
import os
from utils import analytic_solution

def compute_ecm(integrators, dts):
    ecm_dict = {integr: [] for integr in integrators}

    out_folder = "../../outputs/oscillator"
    sims_folder = out_folder + "/sim_results"

    for integr in integrators:
        for dt in dts:
            fn = f"{integr}_{dt}_out.csv"
            filename = os.path.join(sims_folder, fn)
            data = np.genfromtxt(filename, delimiter=",", skip_header=1)  # saltamos la cabecera
            t = data[:, 0]       # columna time
            x_num = data[:, 2]   # columna x
            x_ana, _ = analytic_solution(t)  # calculamos analítica
            ecm = np.mean((x_num - x_ana)**2)  # error cuadrático medio
            ecm_dict[integr].append(ecm)
    return integrators, dts, ecm_dict


def save_ecm_results(integrators, dts, ecm_dict, out_folder):
    """Guarda los resultados de ECM en un CSV."""
    out_file = os.path.join(out_folder, "ecm_results.csv")
    with open(out_file, "w") as f:
        # Encabezado
        f.write("dt," + ",".join(integrators) + "\n")

        # Filas de datos
        for i, dt in enumerate(dts):
            row = [dt]
            for integr in integrators:
                row.append(f"{ecm_dict[integr][i]:.6e}")
            f.write(",".join(row) + "\n")

    print(f"✅ Resultados ECM guardados en: {out_file}")


# Graficar ECM vs dt en escala log-log
def plot(integrators, dts, ecm_dict, fontsize):
    dts_float = [float(dt) for dt in dts]
    out_folder = "outputs/oscillator"

    plt.figure(figsize=(8,5))
    for integr in integrators:
        plt.loglog(dts_float, ecm_dict[integr], marker='o', label=integr)

    plt.xlabel('dt (s)', fontsize=fontsize)
    plt.ylabel('ECM (m²)', fontsize=fontsize)
    plt.grid(True, which="both", ls="--")
    plt.legend(fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.tight_layout()

    out_path = os.path.join(out_folder, "ecm_vs_edt2.png")
    plt.savefig(out_path, dpi=150)
    print(f"✅ Gráfico guardado en: {out_path}")


if __name__ == "__main__":
    integrators = ["gear5", "beeman", "verlet"]
    dts = ["0.1", "0.01", "0.001", "1.0E-4", "1.0E-5", "1.0E-6", "1.0E-7"]
    fontsize = 14

    integrators, dts, ecm_dict = compute_ecm(integrators, dts)
    plot(integrators, dts, ecm_dict, fontsize)
    save_ecm_results(integrators, dts, ecm_dict, "outputs/oscillator")
