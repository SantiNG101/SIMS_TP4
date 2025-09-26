import sys
import numpy as np
import matplotlib.pyplot as plt
import glob, os

def analytic_solution(t, A, m, k, gamma):
    w0 = np.sqrt(k/m)
    beta = gamma/(2*m)
    wd = np.sqrt(w0**2 - beta**2)
    x = A * np.exp(-beta*t) * np.cos(wd*t)
    return x

def compute_ecm(num, ana):
    return np.mean((num - ana)**2)

if len(sys.argv) < 2:
    print("Uso: python error_vs_dt_all.py '<pattern_general>'")
    print("Ejemplo: python error_vs_dt_all.py 'osc_out_dt*.csv'")
    sys.exit(1)

pattern = sys.argv[1]
files = sorted(glob.glob(pattern))

m = 70.0; k = 1e4; gamma = 100.0; A = 1.0

# separo archivos por integrador
groups = {"beeman": [], "gear5": [], "verlet": []}
for fn in files:
    low = fn.lower()
    if "beeman" in low:
        groups["beeman"].append(fn)
    elif "gear5" in low:
        groups["gear5"].append(fn)
    elif "verlet" in low:
        groups["verlet"].append(fn)

plt.figure(figsize=(8,6))

for method, fns in groups.items():
    dts, errors = [], []
    for fn in sorted(fns):
        base = os.path.basename(fn)
        dt = None
        if "dt" in base:
            try:
                dt_str = base.split("dt")[1].split("_")[0]
                dt = float(dt_str.replace("e","E"))
            except Exception:
                dt = None

        data = np.loadtxt(fn, delimiter=",", skiprows=1)
        t = data[:,0]
        x_num = data[:,2]

        x_ana = analytic_solution(t, A, m, k, gamma)
        ecm = compute_ecm(x_num, x_ana)

        if dt is not None:
            dts.append(dt)
            errors.append(ecm)

    if dts:
        plt.loglog(dts, errors, "o-", label=method.capitalize())

plt.xlabel("dt")
plt.ylabel("ECM (posición)")
plt.title("Error cuadrático medio vs dt (comparación de integradores)")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.savefig("error_vs_dt_all.png", dpi=150)
plt.show()

