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
        y_pred = y[i] + h * k1
        k2 = f(t[i] + h, y_pred)
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
def erro_relativo_medio(y_analitico, y_numerico):
    mask = np.abs(y_analitico) > 1e-12
    return np.mean(np.abs((y_analitico[mask] - y_numerico[mask]) / y_analitico[mask]))

# ===========================================
# PARÂMETROS DO PROBLEMA – DESCARGA RC
# ===========================================
V0 = 100.0
C  = 5e-6
R32 = 32e3
R240 = 240e3
R60  = 60e3

Rpar = 1 / (1 / R240 + 1 / R60)
Req = R32 + Rpar
tau = Req * C
t_final = 5 * tau

def f_descarga(t, v):
    return -v / tau

def solucao_analitica(t):
    return V0 * np.exp(-t / tau)

print("\n=== DESCARGA RC ===")
print(f"V0 = {V0} V | Req = {Req:.2f} Ω | τ = {tau:.6f} s | tf = {t_final:.6f} s\n")

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
# TABELA DE RESULTADOS
# ===========================================
print("---------------------------------------------------------------------------------------------------------------")
print("|    h     |   Método    |  V_num_final (V) |  V_ana_final (V) |   ERM (Erro Relativo Médio)   |")
print("---------------------------------------------------------------------------------------------------------------")

for h in hs:
    for nome, metodo in metodos.items():
        t_num, v_num = metodo(f_descarga, 0.0, t_final, V0, h)
        v_ana = solucao_analitica(t_num)
        erm = erro_relativo_medio(v_ana, v_num)
        print(f"| {h:<7.1e} | {nome:<10} | {v_num[-1]:>17.8f} | {v_ana[-1]:>17.8f} | {erm:>25.3e} |")

print("---------------------------------------------------------------------------------------------------------------")

# ===========================================
# CÁLCULO DO ERRO RELATIVO MÉDIO × h
# ===========================================
erro_rk1, erro_rk2, erro_rk3, erro_rk4 = [], [], [], []

for h in hs:
    t, y = rk1(f_descarga, 0.0, t_final, V0, h)
    erro_rk1.append(erro_relativo_medio(solucao_analitica(t), y))

    t, y = rk2(f_descarga, 0.0, t_final, V0, h)
    erro_rk2.append(erro_relativo_medio(solucao_analitica(t), y))

    t, y = rk3(f_descarga, 0.0, t_final, V0, h)
    erro_rk3.append(erro_relativo_medio(solucao_analitica(t), y))

    t, y = rk4(f_descarga, 0.0, t_final, V0, h)
    erro_rk4.append(erro_relativo_medio(solucao_analitica(t), y))

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
    r'$\mathrm{ERM} $',
    fontname='Times New Roman',
    fontsize=14
)
plt.title('')
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend(fontsize=16)
plt.tight_layout()
plt.show()