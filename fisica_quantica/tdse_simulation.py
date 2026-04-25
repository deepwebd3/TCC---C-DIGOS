import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constantes
hbar = 1.0
m = 1.0

# Domínio espacial
L = 10.0
N = 200
x = np.linspace(-L/2, L/2, N)
dx = x[1] - x[0]

# Tempo
dt = 0.001
frames = 600

# Escolha do potencial:
# "harmonic", "barrier" ou "infinite_well"
case = "harmonic"

def potential(x, case="harmonic"):
    if case == "harmonic":
        return 0.5 * x**2

    elif case == "barrier":
        return 10.0 * np.exp(-(x / 0.5)**2)

    elif case == "infinite_well":
        # Dentro do poço: V = 0
        # Fora da região |x| < L/2: V muito alto
        return np.where(np.abs(x) < L/2, 0.0, 1e6)

    else:
        return np.zeros_like(x)

V = potential(x, case)

# Pacote de onda inicial
x0 = -2.0
sigma = 0.5
k0 = 5.0

psi = np.exp(-(x - x0)**2 / (2 * sigma**2)) * np.exp(1j * k0 * x)

# Normalização
psi = psi / np.sqrt(np.sum(np.abs(psi)**2) * dx)

def laplacian(psi):
    lap = np.zeros_like(psi, dtype=complex)
    lap[1:-1] = (psi[2:] - 2 * psi[1:-1] + psi[:-2]) / dx**2
    return lap

def dpsi_dt(psi):
    return -1j / hbar * (
        -(hbar**2 / (2 * m)) * laplacian(psi) + V * psi
    )

def rk4_step(psi, dt):
    k1 = dpsi_dt(psi)
    k2 = dpsi_dt(psi + 0.5 * dt * k1)
    k3 = dpsi_dt(psi + 0.5 * dt * k2)
    k4 = dpsi_dt(psi + dt * k3)

    return psi + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)

# Figura
fig, ax = plt.subplots(figsize=(9, 5))

prob_line, = ax.plot(x, np.abs(psi)**2, label=r"$|\psi(x,t)|^2$")
pot_line, = ax.plot(x, V / np.max(V + 1e-12) * 0.5, "--", label="Potencial normalizado")

ax.set_xlim(x[0], x[-1])
ax.set_ylim(0, 1.2 * np.max(np.abs(psi)**2))
ax.set_xlabel("x")
ax.set_ylabel("Densidade de probabilidade")
ax.set_title(f"Evolução temporal - potencial: {case}")
ax.legend()
ax.grid(True)

def update(frame):
    global psi

    for _ in range(5):
        psi = rk4_step(psi, dt)

        # Condições de contorno
        psi[0] = 0
        psi[-1] = 0

        # Renormalização
        psi = psi / np.sqrt(np.sum(np.abs(psi)**2) * dx)

    prob_line.set_ydata(np.abs(psi)**2)

    return prob_line,

ani = FuncAnimation(fig, update, frames=frames, interval=30, blit=True)

plt.show()