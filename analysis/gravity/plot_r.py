import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

out_folder = "../../outputs/gravity"
sims_folder = out_folder + "/sim_results"
integrator = ""

def compute_rhm(positions):
    """
    Calcula el radio de media masa dado un array (N x 3) de posiciones.
    """
    cm = np.mean(positions, axis=0)  # centro de masa
    dists = np.linalg.norm(positions - cm, axis=1)
    dists_sorted = np.sort(dists)
    rhm = dists_sorted[len(dists)//2]
    return rhm

def compute_rhm_from_file(filename):
    """
    Lee archivo con columnas: time,id,x,y,z,vx,vy,vz
    y devuelve arrays: times, rhm_values
    """
    df = pd.read_csv(filename)
    
    times = []
    rhm_values = []
    
    # agrupar por tiempo
    for t, group in df.groupby("time"):
        positions = group[["x","y","z"]].values
        rhm = compute_rhm(positions)
        times.append(t)
        rhm_values.append(rhm)
    
    return np.array(times), np.array(rhm_values)

def plot_r(filename):
    times, rhm = compute_rhm_from_file(filename)
    
    plt.plot(times, rhm, label="r_hm(t)")
    plt.xlabel("Tiempo")
    plt.ylabel("Radio de media masa")
    plt.legend()
    
    plt.savefig(out_folder+f"/{integrator}/r_dt{dt:.0e}N{N}.png", dpi=150, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    dt = 1e-2
    N = 500
    integrator = "verlet"

    filename = os.path.join(sims_folder, f"{integrator}/out_dt{dt:.0e}N{N}.csv")
    print(f"Filename: {filename}")
    plot_r(filename) 
