import numpy as np
import matplotlib.pyplot as plt

# ============================
# Parâmetros físicos do problema
# ============================
V0 = 30e3       # 30 kV
C = 500e-12     # 500 pF
R_pneu = 100e9  # 100 GΩ
U_fogo = 50e-3  # 50 mJ

R_eq = R_pneu / 4  # Resistência equivalente (4 pneus em paralelo)
tau = R_eq * C      # Constante de tempo

# Função diferencial
def f(V, t):
    return -V / (R_eq * C)

# Solução analítica
def V_analitico(t):
    return V0 * np.exp(-t / tau)

# ============================
# Parâmetros numéricos
# ============================
a, b = 0, 10
Num = 1000
h = (b - a) / Num
t_pontos = np.arange(a, b, h)

# ============================
# 1️⃣ Método de Euler (RK1)
# ============================
V_euler = [V0]
V = V0
for t in t_pontos[:-1]:
    V += h * f(V, t)
    V_euler.append(V)
V_euler = np.array(V_euler)
erro_euler = np.abs((V_euler - V_analitico(t_pontos)) / V_analitico(t_pontos)) * 100

# ============================
# 2️⃣ Método de Runge-Kutta 2ª ordem (Ponto Médio)
# ============================
V_rk2 = [V0]
V = V0
for t in t_pontos[:-1]:
    k1 = h * f(V, t)
    k2 = h * f(V + 0.5 * k1, t + 0.5 * h)
    V += k2
    V_rk2.append(V)
V_rk2 = np.array(V_rk2)
erro_rk2 = np.abs((V_rk2 - V_analitico(t_pontos)) / V_analitico(t_pontos)) * 100

# ============================
# 3️⃣ Método de Runge-Kutta 3ª ordem
# ============================
V_rk3 = [V0]
V = V0
for t in t_pontos[:-1]:
    k1 = h * f(V, t)
    k2 = h * f(V + 0.5 * k1, t + 0.5 * h)
    k3 = h * f(V - k1 + 2 * k2, t + h)
    V += (k1 + 4*k2 + k3) / 6
    V_rk3.append(V)
V_rk3 = np.array(V_rk3)
erro_rk3 = np.abs((V_rk3 - V_analitico(t_pontos)) / V_analitico(t_pontos)) * 100

# ============================
# 4️⃣ Método de Runge-Kutta 4ª ordem
# ============================
V_rk4 = [V0]
V = V0
for t in t_pontos[:-1]:
    k1 = h * f(V, t)
    k2 = h * f(V + 0.5 * k1, t + 0.5 * h)
    k3 = h * f(V + 0.5 * k2, t + 0.5 * h)
    k4 = h * f(V + k3, t + h)
    V += (k1 + 2*k2 + 2*k3 + k4) / 6
    V_rk4.append(V)
V_rk4 = np.array(V_rk4)
erro_rk4 = np.abs((V_rk4 - V_analitico(t_pontos)) / V_analitico(t_pontos)) * 100

# ============================
# Comparação dos erros
# ============================
erro_medio = {
    "Euler": np.mean(erro_euler),
    "RK2": np.mean(erro_rk2),
    "RK3": np.mean(erro_rk3),
    "RK4": np.mean(erro_rk4)
}

erro_max = {
    "Euler": np.max(erro_euler),
    "RK2": np.max(erro_rk2),
    "RK3": np.max(erro_rk3),
    "RK4": np.max(erro_rk4)
}

# ============================
# Gráficos
# ============================
plt.figure(figsize=(14, 6))

# Gráfico do erro relativo (escala log)
plt.semilogy(t_pontos, erro_euler, 'r--', linewidth=1.5, label='Euler (1ª ordem)')
plt.semilogy(t_pontos, erro_rk2, 'b-', linewidth=1.5, label='Runge-Kutta 2ª ordem')
plt.semilogy(t_pontos, erro_rk3, 'g-', linewidth=1.5, label='Runge-Kutta 3ª ordem')
plt.semilogy(t_pontos, erro_rk4, 'purple', linewidth=1.5, label='Runge-Kutta 4ª ordem')

plt.title('Comparação de Erros Relativos — Métodos Numéricos')
plt.xlabel('Tempo (s)')
plt.ylabel('Erro Relativo (%)')
plt.grid(True, which="both", linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# ============================
# Resultados comparativos
# ============================
print("\n" + "="*60)
print("COMPARATIVO DE ERROS — MÉTODOS NUMÉRICOS")
print("="*60)
print(f"Constante de tempo τ = {tau:.6f} s")
print(f"Resistência equivalente: R_eq = {R_eq/1e9:.2f} GΩ")
print(f"Capacitância: C = {C*1e12:.2f} pF\n")

print(f"{'Método':<20}{'Erro médio (%)':<20}{'Erro máximo (%)'}")
print("-"*60)
for metodo in ["Euler", "RK2", "RK3", "RK4"]:
    print(f"{metodo:<20}{erro_medio[metodo]:<20.8f}{erro_max[metodo]:.8f}")