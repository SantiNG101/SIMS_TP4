import numpy as np

# Función de la solución analítica del oscilador amortiguado
def analytic_solution(t, A, m, k, gamma):
    w0 = np.sqrt(k/m)
    beta = gamma/(2*m)
    wd = np.sqrt(w0**2 - beta**2)
    x = A * np.exp(-beta*t) * np.cos(wd*t)
    v = -A * np.exp(-beta*t) * (beta*np.cos(wd*t) + wd*np.sin(wd*t))
    return x, v