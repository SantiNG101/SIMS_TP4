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


def plot_energies(time, E_kin, E_pot, E_tot, dt, integrator):
    """Genera y guarda el gráfico de energías."""

    plt.figure(figsize=(10, 6))

    plt.plot(time, E_kin, linestyle="--", color="tab:blue", label="E_cinética")
    plt.plot(time, E_pot, linestyle="--", color="tab:orange", label="E_potencial")
    plt.plot(time, E_tot, linestyle="-", color="tab:red", label="E_total")

    plt.xlabel("Tiempo")
    plt.ylabel("Energía")
    plt.title(f"Conservación de la Energía (Integrador: {integrator.capitalize()}, $\\Delta t$ = {dt})")
    plt.legend()

    # Dibujamos una línea horizontal de la energía total promedio
    E_tot_avg = np.mean(E_tot)
    plt.axhline(E_tot_avg, color='tab:red', linestyle=':', linewidth=1.5, label=f'$<E_{{tot}}>$')

    plt.grid(True, linestyle=":")

    # Guardamos el archivo en el directorio actual
    plot_filename = f"energies_{integrator}_dt{dt:.0e}.png"
    plt.savefig(plot_filename, dpi=150, bbox_inches="tight")


if __name__ == "__main__":

    # --- CÁLCULO Y GUARDADO DE ENERGÍAS ---
    df_out = pd.read_csv('../../outputs/gravity/sim_results/gear5/out.csv')
    df_out['m'] = 1.0  # Asumiendo m=1.0 para todas las partículas
    energy_filename = 'calculated_energy.csv'
    energy_data = []

    for time_step, group in df_out.groupby('time'):
        ek = calculate_kinetic_energy(group)
        ep = calculate_potential_energy(group, G, h)
        et = ek + ep
        energy_data.append([time_step, ek, ep, et])

    energy_df = pd.DataFrame(energy_data, columns=['Time', 'E_kin', 'E_pot', 'E_tot'])
    energy_df.to_csv(energy_filename, index=False)

    # --- PLOTEO ---
    # Usamos los parámetros del ejemplo de ploteo del usuario
    dt_sim = 1e-3
    integrator_sim = "gear5"

    # Cargamos el archivo que acabamos de generar
    time, E_kin, E_pot, E_tot = load_energy_data(energy_filename)

    # Generamos el gráfico
    plot_energies(time, E_kin, E_pot, E_tot, dt_sim, integrator_sim)

    # Imprimir la variación de energía total para el análisis
    E_tot_initial = E_tot[0]
    E_tot_max = np.max(E_tot)
    E_tot_min = np.min(E_tot)
    delta_E_max = (E_tot_max - E_tot_min) / np.abs(E_tot_initial)