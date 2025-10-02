import numpy as np
import matplotlib.pyplot as plt
import os
import re

out_folder = "../../outputs/gravity"
sims_folder = out_folder + "/sim_results"
integrator = ""

def load_energy_data(filename):

    data = np.loadtxt(filename, delimiter=",", skiprows=1)
    time = data[:, 0]
    E_kin = data[:, 1]
    E_pot = data[:, 2]
    E_tot = data[:, 3]
    return time, E_kin, E_pot, E_tot


def plot_energies(time, E_kin, E_pot, E_tot, dt):
    
    plt.figure(figsize=(8, 5))

    plt.plot(time, E_kin, linestyle="--", color="tab:blue", label="E_kin")
    plt.plot(time, E_pot, linestyle="--", color="tab:orange", label="E_pot")
    plt.plot(time, E_tot, linestyle="-", color="tab:red", label="E_tot")

    plt.xlabel("Tiempo")
    plt.ylabel("Energía")
    plt.title(f"Energías del sistema (dt = {dt:.0e})")
    plt.legend()
    plt.grid(True, linestyle=":")


    plt.savefig(out_folder+f"/{integrator}/energies_dt{dt:.0e}N{N}.png", dpi=150, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    
    dt = 1e-3
    N= 200
    integrator = "verlet"

    filename = os.path.join(sims_folder, f"{integrator}/energy/energy_dt{dt:.0e}N{N}.csv")
    print(f"Filename: {filename}")

    time, E_kin, E_pot, E_tot = load_energy_data(filename)
    plot_energies(time, E_kin, E_pot, E_tot, dt)

