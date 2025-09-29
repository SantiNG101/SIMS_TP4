import numpy as np

# Parámetros del problema (de Main.java)
m = 70.0
k = 1e4
gamma = 100.0
A = 1.0

# Función de la solución analítica del oscilador amortiguado
def analytic_solution(t):
    w0 = np.sqrt(k/m)
    beta = gamma/(2*m)
    wd = np.sqrt(w0**2 - beta**2)
    x = A * np.exp(-beta*t) * np.cos(wd*t)
    v = -A * np.exp(-beta*t) * (beta*np.cos(wd*t) + wd*np.sin(wd*t))
    return x, v