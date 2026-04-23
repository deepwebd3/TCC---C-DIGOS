# ================================================================
# ANÁLISE DE CIRCUITOS RC COM O MÉTODO DE RUNGE-KUTTA DE 4ª ORDEM
# Exemplos baseados em: NILSSON, J.W.; RIEDEL, S. Electric Circuits, 10ª ed.
#   - Example 7.3 (descarga RC - resposta natural)
#   - Example 7.8 (carga RC - resposta ao degrau)
# ================================================================

import numpy as np
import matplotlib.pyplot as plt

# ================================================================
# Função genérica do método de Runge-Kutta 4ª ordem
# ================================================================
def rk4(f, t0, tf, y0, h):
    n = int((tf - t0) / h)
    t = np.linspace(t0, tf, n+1)
    y = np.zeros(n+1)
    y[0] = y0

    for i in range(n):
        k1 = f(t[i], y[i])
        k2 = f(t[i] + h/2, y[i] + h/2 * k1)
        k3 = f(t[i] + h/2, y[i] + h/2 * k2)
        k4 = f(t[i] + h, y[i] + h * k3)
        y[i+1] = y[i] + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    return t, y

# ================================================================
# Função auxiliar: cálculo do Erro Percentual Médio (EPM)
# ================================================================
def erro_percentual_medio(y_analitico, y_numerico):
    return np.mean(np.abs((y_analitico - y_numerico) / y_analitico)) * 100

# ================================================================
# EXEMPLO A — Resposta natural (descarga do capacitor)
# (NILSSON, Example 7.3)
# ================================================================
R_eq = 60e3     # 60 kΩ
C = 0.5e-3      # 0.5 mF
V0 = 5.0        # tensão inicial (V)
tau = R_eq * C  # constante de tempo
t_final = 5 * tau  # simular até 5 constantes de tempo
h = tau / 100   # passo

# Equação diferencial: dV/dt = -1/(R_eq*C)*V
def f_descarga(t, V):
    return -V / (R_eq * C)

# Solução analítica
t_analitico = np.linspace(0, t_final, 1000)
v_analitico = V0 * np.exp(-t_analitico / tau)

# Solução numérica RK4
t_rk, v_rk = rk4(f_descarga, 0, t_final, V0, h)

# Erro percentual médio
epm_A = erro_percentual_medio(np.interp(t_rk, t_analitico, v_analitico), v_rk)

# Plot
plt.figure(figsize=(8,5))
plt.plot(t_analitico*1000, v_analitico, 'b-', label='Solução Analítica')
plt.plot(t_rk*1000, v_rk, 'ro', label='RK4', markersize=4)
plt.title('Exemplo A – Descarga RC (Nilsson, Ex. 7.3)')
plt.xlabel('Tempo (ms)')
plt.ylabel('Tensão no Capacitor (V)')
plt.grid(True)
plt.legend()
plt.show()

print(f"EPM (Exemplo A) = {epm_A:.6f} %")

# ================================================================
# EXEMPLO B — Resposta ao degrau (carga do capacitor)
# (NILSSON, Example 7.8)
# ================================================================
V_th = 150.0    # tensão final (V)
tau_B = 5e-3    # constante de tempo 5 ms (R_eq*C)
h_B = tau_B / 50
t_final_B = 5 * tau_B  # até 5τ
V0_B = 0.0      # condição inicial

# Equação diferencial: dV/dt = (V_th - V)/(R_eq*C)
# Como R_eq*C = tau_B, podemos simplificar:
def f_carga(t, V):
    return (V_th - V) / tau_B

# Solução analítica
t_analitico_B = np.linspace(0, t_final_B, 1000)
v_analitico_B = V_th * (1 - np.exp(-t_analitico_B / tau_B))

# Solução numérica RK4
t_rk_B, v_rk_B = rk4(f_carga, 0, t_final_B, V0_B, h_B)

# Erro percentual médio
epm_B = erro_percentual_medio(np.interp(t_rk_B, t_analitico_B, v_analitico_B), v_rk_B)

# Plot
plt.figure(figsize=(8,5))
plt.plot(t_analitico_B*1000, v_analitico_B, 'b-', label='Solução Analítica')
plt.plot(t_rk_B*1000, v_rk_B, 'ro', label='RK4', markersize=4)
plt.title('Exemplo B – Carga RC (Nilsson, Ex. 7.8)')
plt.xlabel('Tempo (ms)')
plt.ylabel('Tensão no Capacitor (V)')
plt.grid(True)
plt.legend()
plt.show()

print(f"EPM (Exemplo B) = {epm_B:.6f} %")