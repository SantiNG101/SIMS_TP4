import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter

def animate_cumulus(integratorName="verlet"):
    out_folder = "outputs/gravity/"
    sim_folder = out_folder + "cumulus/" + integratorName + "/"
    df = pd.read_csv(sim_folder + "out.csv")

    N = df['id'].nunique()
    N1 = N // 2  # 2 cúmulos

    colors = ['red']*N1 + ['blue']*N1

    times = df['time'].unique()

    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')

    first_frame = df[df['time'] == times[0]].sort_values('id')

    scat = ax.scatter(
        first_frame['x'], first_frame['y'], first_frame['z'],
        s=20, c=colors
    )

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-5, 5)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Función de actualización para cada frame
    def update(frame):
        t = times[frame]
        data = df[df['time'] == t].sort_values('id')
        scat._offsets3d = (data['x'], data['y'], data['z'])
        ax.set_title(f"t = {t:.2f} s")
        return scat,

    ani = FuncAnimation(fig, update, frames=len(times), interval=50, blit=False)

    ani.save(sim_folder + "collision_cumulus.gif", writer=PillowWriter(fps=20))


if __name__ == "__main__":

    integratorName = "verlet"  # "verlet", "beeman", "gear5"

    animate_cumulus(integratorName)