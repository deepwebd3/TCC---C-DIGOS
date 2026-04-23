import os
import numpy as np
import matplotlib.pyplot as plt

# ===========================================
# MÉTODOS DE RUNGE-KUTTA
# ===========================================
def rk1(f, t0, tf, y0, h):
    n = int(round((tf - t0) / h))
    t = np.linspace(t0, tf, n + 1)
    y = np.zeros(n + 1)
    y[0] = y0
    for i in range(n):
        y[i + 1] = y[i] + h * f(t[i], y[i])
    return t, y

def rk2(f, t0, tf, y0, h):
    n = int(round((tf - t0) / h))
    t = np.linspace(t0, tf, n + 1)
    y = np.zeros(n + 1)
    y[0] = y0
    for i in range(n):
        k1 = f(t[i], y[i])
        k2 = f(t[i] + h, y[i] + h * k1)
        y[i + 1] = y[i] + (h / 2) * (k1 + k2)
    return t, y

def rk3(f, t0, tf, y0, h):
    n = int(round((tf - t0) / h))
    t = np.linspace(t0, tf, n + 1)
    y = np.zeros(n + 1)
    y[0] = y0
    for i in range(n):
        k1 = f(t[i], y[i])
        k2 = f(t[i] + h / 2, y[i] + h * k1 / 2)
        k3 = f(t[i] + h, y[i] - h * k1 + 2 * h * k2)
        y[i + 1] = y[i] + h * (k1 + 4 * k2 + k3) / 6
    return t, y

def rk4(f, t0, tf, y0, h):
    n = int(round((tf - t0) / h))
    t = np.linspace(t0, tf, n + 1)
    y = np.zeros(n + 1)
    y[0] = y0
    for i in range(n):
        k1 = f(t[i], y[i])
        k2 = f(t[i] + h / 2, y[i] + h * k1 / 2)
        k3 = f(t[i] + h / 2, y[i] + h * k2 / 2)
        k4 = f(t[i] + h, y[i] + h * k3)
        y[i + 1] = y[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    return t, y

# ===========================================
# FUNÇÃO DE ERRO RELATIVO MÉDIO
# ===========================================
def erro_relativo_medio(y_exato, y_num):
    mask = np.abs(y_exato) > 1e-12
    return np.mean(np.abs((y_exato[mask] - y_num[mask]) / y_exato[mask]))

# ===========================================
# PARÂMETROS – CARGA RC
# ===========================================
Is = 7.5e-3
R1 = 20e3
C  = 5e-6

V_th = Is * R1
tau  = R1 * C
t_final = 1.0

def f_carga(t, v):
    return (V_th - v) / tau

def solucao_analitica(t):
    return V_th * (1 - np.exp(-t / tau))

print("\n=== CARGA RC ===")
print(f"V_th = {V_th:.2f} V | τ = {tau:.6f} s | tf = {t_final:.2f} s\n")

# ===========================================
# MÉTODOS E TAMANHOS DE PASSO
# ===========================================
metodos = {
    "RK1 (Euler)": rk1,
    "RK2 (Heun)": rk2,
    "RK3": rk3,
    "RK4": rk4
}

hs = [0.001, 0.0001, 0.00001]

# ===========================================
# CÁLCULO DO ERRO RELATIVO MÉDIO × h
# ===========================================
erro_rk1, erro_rk2, erro_rk3, erro_rk4 = [], [], [], []

for h in hs:
    t, y = rk1(f_carga, 0.0, t_final, 0.0, h)
    erro_rk1.append(erro_relativo_medio(solucao_analitica(t), y))

    t, y = rk2(f_carga, 0.0, t_final, 0.0, h)
    erro_rk2.append(erro_relativo_medio(solucao_analitica(t), y))

    t, y = rk3(f_carga, 0.0, t_final, 0.0, h)
    erro_rk3.append(erro_relativo_medio(solucao_analitica(t), y))

    t, y = rk4(f_carga, 0.0, t_final, 0.0, h)
    erro_rk4.append(erro_relativo_medio(solucao_analitica(t), y))

# ===========================================
# CAMINHO DE SAÍDA
# ===========================================
pasta_base = os.path.dirname(os.path.dirname(__file__))
pasta_saida = os.path.join(pasta_base, "GRAFICOS_PNG")
os.makedirs(pasta_saida, exist_ok=True)
arquivo_saida = os.path.join(pasta_saida, "grafico3.png")

# ===========================================
# GRÁFICO FINAL: ERM × h
# ===========================================
plt.figure(figsize=(10, 5))

plt.plot(hs, erro_rk1, marker='o', label='RK1 (Euler)')
plt.plot(hs, erro_rk2, marker='o', label='RK2 (Heun)')
plt.plot(hs, erro_rk3, marker='o', label='RK3')
plt.plot(hs, erro_rk4, marker='o', label='RK4')

plt.xscale('log')
plt.yscale('log')
plt.xlabel(
    r'$\mathrm{Passo}\ h$',
    fontname='Times New Roman',
    fontsize=14
)
plt.ylabel(
    r'$\mathrm{ERM}$',
    fontname='Times New Roman',
    fontsize=14
)
plt.title("")
plt.grid(True, which="both", linestyle="--", alpha=0.6)
plt.legend(fontsize=16)
plt.tight_layout()
plt.savefig(arquivo_saida, dpi=300, bbox_inches="tight")
plt.show()
plt.close()