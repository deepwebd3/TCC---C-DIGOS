import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# PARÂMETROS DO PROBLEMA
# =====================================================
C = 500e-12
V0 = 30e3
R_pneu = 100e9

R_eq = R_pneu / 4
tau = R_eq * C

def f(V, t):
    return -V / (R_eq * C)

# =====================================================
# INTERVALO DE TEMPO
# =====================================================
a, b = 0.0, 10.0
eps = np.finfo(float).eps

# =====================================================
# TAMANHOS DE PASSO
# =====================================================
h_list = [0.1, 0.01, 0.001]

# =====================================================
# MÉTODOS DE RUNGE-KUTTA
# =====================================================
def euler(V0, t, h):
    V = np.zeros(len(t))
    V[0] = V0
    for i in range(1, len(t)):
        V[i] = V[i-1] + h * f(V[i-1], t[i-1])
    return V

def rk2(V0, t, h):
    V = np.zeros(len(t))
    V[0] = V0
    for i in range(1, len(t)):
        k1 = f(V[i-1], t[i-1])
        k2 = f(V[i-1] + 0.5*h*k1, t[i-1] + 0.5*h)
        V[i] = V[i-1] + h * k2
    return V

def rk3(V0, t, h):
    V = np.zeros(len(t))
    V[0] = V0
    for i in range(1, len(t)):
        k1 = h * f(V[i-1], t[i-1])
        k2 = h * f(V[i-1] + 0.5*k1, t[i-1] + 0.5*h)
        k3 = h * f(V[i-1] - k1 + 2*k2, t[i-1] + h)
        V[i] = V[i-1] + (k1 + 4*k2 + k3) / 6
    return V

def rk4(V0, t, h):
    V = np.zeros(len(t))
    V[0] = V0
    for i in range(1, len(t)):
        k1 = h * f(V[i-1], t[i-1])
        k2 = h * f(V[i-1] + 0.5*k1, t[i-1] + 0.5*h)
        k3 = h * f(V[i-1] + 0.5*k2, t[i-1] + 0.5*h)
        k4 = h * f(V[i-1] + k3, t[i-1] + h)
        V[i] = V[i-1] + (k1 + 2*k2 + 2*k3 + k4) / 6
    return V

# =====================================================
# CÁLCULO DO ERRO RELATIVO MÉDIO
# =====================================================
erro_medio_euler = []
erro_medio_rk2   = []
erro_medio_rk3   = []
erro_medio_rk4   = []

for h in h_list:
    t = np.arange(a, b + h, h)
    V_analitico = V0 * np.exp(-t / tau)

    erro_medio_euler.append(
        np.mean(np.abs(euler(V0, t, h) - V_analitico) /
                np.maximum(np.abs(V_analitico), eps))
    )

    erro_medio_rk2.append(
        np.mean(np.abs(rk2(V0, t, h) - V_analitico) /
                np.maximum(np.abs(V_analitico), eps))
    )

    erro_medio_rk3.append(
        np.mean(np.abs(rk3(V0, t, h) - V_analitico) /
                np.maximum(np.abs(V_analitico), eps))
    )

    erro_medio_rk4.append(
        np.mean(np.abs(rk4(V0, t, h) - V_analitico) /
                np.maximum(np.abs(V_analitico), eps))
    )

# =====================================================
# GRÁFICO FINAL: ERM x h
# =====================================================
plt.figure(figsize=(10, 5))

plt.plot(h_list, erro_medio_euler, marker='o', label='RK1 (Euler)')
plt.plot(h_list, erro_medio_rk2,   marker='o', label='RK2 (Heun)')
plt.plot(h_list, erro_medio_rk3,   marker='o', label='RK3')
plt.plot(h_list, erro_medio_rk4,   marker='o', label='RK4')

plt.xscale('log')
plt.yscale('log')
plt.xlabel(
    r'$\mathrm{Passo}\ h$',
    fontname='Times New Roman',
    fontsize=14
)
plt.ylabel(
    r'$\mathrm{ERM} $',
    fontname='Times New Roman',
    fontsize=14
)
plt.title('')
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend(fontsize=16)
plt.tight_layout()
plt.show()