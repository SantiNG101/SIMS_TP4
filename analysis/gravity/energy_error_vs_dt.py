import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_energies(integrator, dts_list, N, fontsize):
    data_dir = f"outputs/gravity/sim_results/{integrator}/"

    errors_mean = []
    errors_std = []
    dts = []

    for dt in dts_list:
        filename = os.path.join(
            data_dir,
            f"dt{dt:.0e}N{N}",
            f"energy.csv"
        )

        df = pd.read_csv(filename)
        E_tot = df["E_tot"].values
        E0 = E_tot[0]

        # error relativo medio
        errors_t = np.abs(E_tot - E0) / abs(E0)
        error_mean = np.mean(errors_t)
        error_std = np.std(errors_t)

        dts.append(dt)
        errors_mean.append(error_mean)
        errors_std.append(error_std)

    dts, errors_mean, errors_std = zip(*sorted(zip(dts, errors_mean, errors_std)))

    plt.figure(figsize=(7,5))

    plt.errorbar(
        dts, 
        errors_mean, 
        yerr=errors_std, 
        fmt='o-', 
        capsize=5, 
        label="Error relativo energía"
    )
   
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("dt (s)", fontsize=fontsize)
    plt.ylabel("Error relativo promedio de energía total", fontsize=fontsize)
    plt.grid(True, which="both", ls=":")
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.savefig(f"outputs/gravity/energy_error_vs_dt_{integrator}.png", dpi=150, bbox_inches="tight")


if __name__ == "__main__":

    # PARÁMETROS DE SIMULACIÓN (ajustar según sea necesario)
    dts = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5]
    N = 200 
    integrator = "verlet"
    fontsize = 14

    plot_energies(integrator, dts, N, fontsize)