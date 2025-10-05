import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# --- PARÁMETROS DEL SISTEMA (según el código Java) ---
G = 1.0  # Constante de gravitación
h = 0.05  # Parámetro de suavizado


# --- FUNCIONES DE CÁLCULO DE ENERGÍA ---

def calculate_kinetic_energy(df):
    """
    Calcula la energía cinética total del sistema para un paso de tiempo.
    E_k = 0.5 * m * |v|^2
    """
    m = df['m'].values
    vx = df['vx'].values
    vy = df['vy'].values
    vz = df['vz'].values

    ek = 0.5 * np.sum(m * (vx ** 2 + vy ** 2 + vz ** 2))
    return ek


def calculate_potential_energy(df_particles, G, h):
    """
    Calcula la energía potencial total del sistema con suavizado de Plummer.
    E_p = -G * m1 * m2 / sqrt(r^2 + h^2)
    """
    ep = 0.0

    particles = df_particles.to_dict('records')
    n = len(particles)
    h2 = h ** 2

    for i in range(n):
        for j in range(i + 1, n):
            p1 = particles[i]
            p2 = particles[j]

            dx = p1['x'] - p2['x']
            dy = p1['y'] - p2['y']
            dz = p1['z'] - p2['z']
            dist_squared = dx ** 2 + dy ** 2 + dz ** 2

            dist_softened = np.sqrt(dist_squared + h2)
            ep += -G * p1['m'] * p2['m'] / dist_softened

    return ep


# --- ADAPTACIÓN DE LAS FUNCIONES DEL USUARIO PARA CARGA Y PLOTEO ---

def load_energy_data(filename):
    """Carga los datos de energía del archivo CSV."""
    data = pd.read_csv(filename)
    time = data['Time'].values
    E_kin = data['E_kin'].values
    E_pot = data['E_pot'].values
    E_tot = data['E_tot'].values
    return time, E_kin, E_pot, E_tot


def plot_energies(time, E_kin, E_pot, E_tot, dt, integrator, fontsize):
    """Genera y guarda el gráfico de energías."""

    plt.figure(figsize=(10, 6))

    plt.plot(time, E_kin, linestyle="--", color="tab:blue", label="Energía cinética")
    plt.plot(time, E_pot, linestyle="--", color="tab:orange", label="Energía potencial")
    plt.plot(time, E_tot, linestyle="-", color="tab:red", label="Energía total")

    plt.xlabel("Tiempo (s)", fontsize=fontsize)
    plt.ylabel("Energía (J)", fontsize=fontsize)
    plt.legend(fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)

    # Dibujamos una línea horizontal de la energía total promedio
    E_tot_avg = np.mean(E_tot)
    plt.axhline(E_tot_avg, color='tab:red', linestyle=':', linewidth=1.5, label=f'$<E_{{tot}}>$')

    plt.grid(True, linestyle=":")

    # Guardamos el archivo en el directorio actual
    plot_filename = f"outputs/gravity/energy_{integrator}_dt{dt}.png"
    plt.savefig(plot_filename, dpi=150, bbox_inches="tight")


if __name__ == "__main__":

    # ---------------------------------------------------------------------------------------------------------------
    
    # PARÁMETROS DE SIMULACIÓN (ajustar según sea necesario)
    integrator = "verlet"
    dt_list = ["1e-05"]
    N = 200 
    fontsize = 15

    # ---------------------------------------------------------------------------------------------------------------
    
    for dt in dt_list:
        sim_dir = f'outputs/gravity/sim_results/{integrator}/dt{dt}N{N}'
        out_dir = os.path.join(sim_dir, 'out')

        # agarro el primer archivo CSV de la carpeta out
        files = os.listdir(out_dir)
        first_file = sorted(files)[0]

        file_path = os.path.join(out_dir, first_file)

        # leer CSV
        df_out = pd.read_csv(file_path)
        df_out['m'] = 1.0  # Asumiendo m=1.0 para todas las partículas
        energy_filename = sim_dir + f"/energy.csv"
        energy_data = []

        for time_step, group in df_out.groupby('time'):
            ek = calculate_kinetic_energy(group)
            ep = calculate_potential_energy(group, G, h)
            et = ek + ep
            energy_data.append([time_step, ek, ep, et])

        energy_df = pd.DataFrame(energy_data, columns=['Time', 'E_kin', 'E_pot', 'E_tot'])
        energy_df.to_csv(energy_filename, index=False)

        # --- PLOTEO ---

        # Cargamos el archivo que acabamos de generar
        time, E_kin, E_pot, E_tot = load_energy_data(energy_filename)

        # Generamos el gráfico
        plot_energies(time, E_kin, E_pot, E_tot, dt, integrator, fontsize)