import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# -----------------------------
# Configuración de archivos
# -----------------------------
script_dir = os.path.dirname(__file__)

# CSV de entrada: primer argumento o default
csv_file = os.path.join(script_dir, '..', 'osc_out.csv')

# Archivo de salida GIF: segundo argumento o default
out_file = 'anim.gif'

# -----------------------------
# Leer datos del CSV
# -----------------------------
data = {}
times = []

with open(csv_file) as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split(',')
        t = float(parts[0])
        pid = int(parts[1])
        x = float(parts[2])
        y = float(parts[3])
        z = float(parts[4])

        if t not in data:
            data[t] = {}
            times.append(t)
        data[t][pid] = (x, y, z)

times = sorted(times)
N = max(len(data[t]) for t in times)

# -----------------------------
# Construir frames
# -----------------------------
frames = []
for t in times:
    arr = np.zeros((N, 3))
    for pid, (x, y, z) in data[t].items():
        arr[pid] = [x, y, z]
    frames.append(arr)

# -----------------------------
# Crear figura y scatter
# -----------------------------
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
sc = ax.scatter(frames[0][:, 0], frames[0][:, 1], s=5)
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

def update(i):
    sc.set_offsets(frames[i][:, :2])
    ax.set_title(f't={times[i]:.3g}')
    return sc,

ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=30)

# -----------------------------
# Guardar animación como GIF usando Pillow
# -----------------------------
ani.save(out_file, writer='pillow', fps=30)

print('Saved', out_file)

