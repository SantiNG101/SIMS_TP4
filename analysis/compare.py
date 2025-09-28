import numpy as np
import os
import matplotlib.pyplot as plt

def analytic_solution(t, A, m, k, gamma):
    w0 = np.sqrt(k/m)
    beta = gamma/(2*m)
    wd = np.sqrt(w0**2 - beta**2)
    x = A * np.exp(-beta*t) * np.cos(wd*t)
    return x

# parámetros del oscilador
m = 70.0
k = 1e4
gamma = 100.0
A = 1.0

out_folder = "outputs/oscillator"
sims_folder = out_folder + "/sim_results"

out = os.path.join(out_folder, "compare_integrators_zoom.png")

# archivos de salida de cada integrador (ajustá rutas si hace falta)
files = {
    "Gear5": os.path.join(sims_folder, "gear5_out.csv"),
    "Beeman": os.path.join(sims_folder, "beeman_out.csv"),
    "Verlet": os.path.join(sims_folder, "verlet_out.csv"),
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
x_ana_curve = analytic_solution(t_ref, A, m, k, gamma)

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
plt.show()


