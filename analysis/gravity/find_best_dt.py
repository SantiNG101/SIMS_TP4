import numpy as np
import matplotlib.pyplot as plt
import os
import re

out_folder = "../../outputs/gravity"
sims_main_folder = out_folder + "/sim_results/"

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

    plt.savefig(out_folder + f"/energies_dt{dt:.0e}.png", dpi=150, bbox_inches="tight")
    plt.close()

def compute_energy_error(E_tot):
    E0 = E_tot[0]
    return np.max(np.abs((E_tot - E0) / np.abs(E0)))

def analyze_all_sims(threshold=1e-3, integrator="verlet"):
    results = []
    dt_pattern = re.compile(r"energy_dt([0-9.eE+-]+)\.csv")
    sims_folder = sims_main_folder + integrator

    for fname in os.listdir(sims_folder):
        match = dt_pattern.match(fname)
        if match:
            dt = float(match.group(1))
            filepath = os.path.join(sims_folder, fname)
            time, E_kin, E_pot, E_tot = load_energy_data(filepath)

            error = compute_energy_error(E_tot)
            results.append((dt, error, time, E_kin, E_pot, E_tot))

    # ordenar por dt ascendente
    results.sort(key=lambda x: x[0])

    # elegir el mejor
    best = None
    for dt, error, *_ in results:
        if error < threshold:
            best = (dt, error)
            break

    # gráfico comparativo error vs dt
    plt.figure(figsize=(7, 5))
    plt.loglog([r[0] for r in results], [r[1] for r in results], "o-", label="Error relativo")
    plt.axhline(threshold, color="red", linestyle="--", label=f"Umbral = {threshold}")
    plt.xlabel("dt")
    plt.ylabel("max|ΔE/E0|")
    plt.title("Error relativo de energía según dt")
    plt.legend()
    plt.grid(True, which="both", linestyle=":")
    plt.savefig(out_folder + "/energy_conservation_vs_dt.png", dpi=150, bbox_inches="tight")
    plt.close()

    return results, best

if __name__ == "__main__":
    threshold = 1e-3  # lo podés cambiar desde acá
    integrator = "verlet"

    results, best = analyze_all_sims(threshold, integrator)

    print("Resultados de conservación:")
    for dt, error, *_ in results:
        print(f" dt = {dt:.0e}, error = {error:.3e}")

    if best:
        print(f"\n>> Mejor dt según umbral {threshold} usando el integrador {integrator}: dt = {best[0]:.0e}, error = {best[1]:.3e}")
    else:
        print(f"\n>> Ningún dt cumple con el umbral {threshold} usando el integrador {integrator}")
