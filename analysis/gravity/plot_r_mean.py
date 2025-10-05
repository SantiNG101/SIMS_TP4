import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

out_folder = "../../outputs/gravity"
sims_folder = out_folder + "/sim_results"
integrator = "verlet"

def compute_rhm(positions):
    cm = np.mean(positions, axis=0)
    dists = np.linalg.norm(positions - cm, axis=1)
    dists_sorted = np.sort(dists)
    rhm = dists_sorted[len(dists)//2]
    return rhm

def compute_rhm_from_file(filename):
    df = pd.read_csv(filename)
    times = []
    rhm_values = []
    for t, group in df.groupby("time"):
        positions = group[["x","y","z"]].values
        rhm = compute_rhm(positions)
        times.append(t)
        rhm_values.append(rhm)
    return np.array(times), np.array(rhm_values)

def compute_average_rhm(file_list, t_transient):
    if len(file_list) == 0:
        raise ValueError("No hay simulaciones en la lista")

    all_rhms = []
    slopes_indiv = []

    for f in file_list:
        times, rhm = compute_rhm_from_file(f)

        mask_stat = times >= t_transient
        times_stat = times[mask_stat]
        rhm_stat = rhm[mask_stat]

        all_rhms.append(rhm)

        # pendiente individual de esta sim
        slope, intercept = np.polyfit(times_stat, rhm_stat, 1)
        slopes_indiv.append(slope)

    arr = np.vstack(all_rhms)  # (n_sims, n_times)
    mean_full = np.mean(arr, axis=0)
    std_full = np.std(arr, axis=0)

    mask_stat = times >= t_transient
    mean_stat = mean_full[mask_stat]
    std_stat = std_full[mask_stat]
    times_stat = times[mask_stat]

    # pendiente sobre el promedio
    slope_mean, intercept_mean = np.polyfit(times_stat, mean_stat, 1)
        # si quiero que tome la ultima parte del estacionario: slope_from_tail(times_stat,mean_stat,frac_tail_for_slope)
    slope_std = np.std(slopes_indiv)

    return (
        times,
        mean_full, 
        std_full,
        times_stat,
        mean_stat,
        std_stat,
        slope_mean,
        slope_std,
        intercept_mean
    )

def slope_from_tail(times_tail, rhm_tail, frac_tail):
    n = len(times_tail)
    start_idx = int(n * (1 - frac_tail))
    t_fit = times_tail[start_idx:]
    y_fit = rhm_tail[start_idx:]
    p = np.polyfit(t_fit, y_fit, 1)
    return p[0], p[1]  # slope, intercept

def analyze_all_N(N_values, dt, t_transient, frac_tail_for_slope):
    slopes_values = []
    slopes_std_values = []
    Ns_ok = []
    
    # PRIMERA PASADA: calcular el máximo valor de r_hm para establecer escala común
    max_rhm = 0
    all_data = []  # para almacenar datos temporales
    
    for N in N_values:
        folder = os.path.join(sims_folder, integrator, f"dt{dt:.0e}N{N}/out")
        file_list = sorted(glob.glob(os.path.join(folder, "*.csv")))
        print(f"N={N}: {len(file_list)} simulaciones")

        if len(file_list) == 0:
            continue

        times, mean_full, std_full, times_stat, mean_stat, std_stat, slope_mean, slope_std, intercept_mean = compute_average_rhm(
            file_list, t_transient=t_transient
        )
        
        # Guardo datos para segunda pasada
        all_data.append({
            'N': N,
            'times': times,
            'mean_full': mean_full,
            'std_full': std_full,
            'times_stat': times_stat,
            'mean_stat': mean_stat,
            'std_stat': std_stat,
            "slope_mean": slope_mean,
            "slope_std": slope_std,
            "intercept_mean": intercept_mean,
            'file_list': file_list
        })
        
        # Actualizo máximo valor de r_hm
        current_max = np.max(mean_full + std_full)
        if current_max > max_rhm:
            max_rhm = current_max
    
    # Añadi un margen del 10% para q se vea mejor
    y_max = max_rhm * 1.1
    
    # SEGUNDA PASADA: generar gráficos con escala común
    for data in all_data:
        N = data['N']
        times = data['times']
        mean_full = data['mean_full']
        std_full = data['std_full']
        times_stat = data['times_stat']
        mean_stat = data['mean_stat']
        slope_mean = data['slope_mean']
        slope_std = data['slope_std']
        intercept_mean = data['intercept_mean']

        slope = slope_mean
        slopes_values.append(slope_mean)
        slopes_std_values.append(slope_std)
        print(slopes_std_values)
        Ns_ok.append(N)

        # plot promedio y ajuste con escala común
        plt.figure(figsize=(7,4))
        plt.plot(times, mean_full, label=f"<r_hm>(N={N})")
        plt.fill_between(times, mean_full-std_full, mean_full+std_full, alpha=0.25)
        plt.axvline(t_transient, color='gray', linestyle='--', label="t_transient")
        t_line = np.array([times_stat[0], times_stat[-1]])
        plt.plot(t_line, intercept_mean + slope*t_line, 'r--', label=f"slope={slope:.2e}")
        
        # Estableci escala común en Y
        plt.ylim(0, y_max)
        
        plt.xlabel("dt (s)")
        plt.ylabel("<r_hm> (m)")
        plt.legend()
        os.makedirs(out_folder + f"/{integrator}", exist_ok=True)
        plt.savefig(out_folder + f"/{integrator}/rhm_avg_N{N}_dt{dt:.0e}.png", dpi=150)
        plt.close()

    # pendiente vs N
    if Ns_ok:
        plt.figure(figsize=(6,4))
        plt.errorbar(Ns_ok, slopes_values, yerr= slopes_std_values, fmt='o-', capsize=5)
        plt.xlabel("N")
        plt.ylabel("Pendiente de <r_hm> en estado estacionario")
        plt.grid(True)
        plt.savefig(out_folder + f"/{integrator}/slope_vs_N_dt{dt:.0e}.png", dpi=150)
        plt.show()

    return Ns_ok, slopes_values

# ---------------- Uso ----------------
if __name__ == "__main__":
    N_values = [100, 200, 500, 1000, 1500, 2000]
    dt = 1e-3
    t_transient = 0.5
    frac_tail_for_slope = t_transient #0.5

    Ns, slopes = analyze_all_N(N_values, dt=dt, t_transient=t_transient, frac_tail_for_slope=frac_tail_for_slope)
    print("Pendientes calculadas:")
    for n, s in zip(Ns, slopes):
        print(f" N={n}: slope={s:.3e}")