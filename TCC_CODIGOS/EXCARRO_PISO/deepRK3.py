import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# PARÂMETROS DO PROBLEMA
# =====================================================
U_fogo = 50e-3   # 50 mJ (energia crítica)
V0 = 30e3        # 30 kV (tensão inicial)
C = 500e-12      # 500 pF (capacitância)
R_pneu = 100e9   # 100 GΩ (resistência de cada pneu)

# Resistência equivalente (4 pneus em paralelo)
R_eq = R_pneu / 4

# Função diferencial: dV/dt = -V/(R_eq*C)
def f(V, t):
    return -V / (R_eq * C)

# Energia armazenada no capacitor
def energia(V):
    return 0.5 * C * V**2

# =====================================================
# PARÂMETROS DA SIMULAÇÃO
# =====================================================
a = 0
b = 10           # tempo final
Num = 1000
h = (b - a) / Num
V = V0

# Vetores de armazenamento
t_pontos = np.arange(a, b, h)
V_pontos, U_pontos, erro_relativo = [], [], []
tempo_critico = None

# =====================================================
# MÉTODO DE RUNGE-KUTTA DE 3ª ORDEM (RK3)
# =====================================================
for t in t_pontos:
    V_pontos.append(V)
    U = energia(V)
    U_pontos.append(U)

    # Solução analítica instantânea
    V_analitico = V0 * np.exp(-t / (R_eq * C))
    erro = abs(V - V_analitico) / abs(V_analitico)
    erro_relativo.append(erro)

    # Verifica se atingiu a energia crítica
    if U <= U_fogo and tempo_critico is None:
        tempo_critico = t
        print(f"\n=== TEMPO CRÍTICO ALCANÇADO (NUMÉRICO) ===")
        print(f"t = {t:.6f} s")
        print(f"Tensão numérica: V = {V:.6e} V")
        print(f"Tensão analítica: V_analítico = {V_analitico:.6e} V")
        print(f"Energia numérica: U = {U:.8e} J\n")

    # Coeficientes RK3
    k1 = h * f(V, t)
    k2 = h * f(V + 0.5 * k1, t + 0.5 * h)
    k3 = h * f(V - k1 + 2 * k2, t + h)
    V += (k1 + 4 * k2 + k3) / 6

# =====================================================
# SOLUÇÃO ANALÍTICA DE REFERÊNCIA
# =====================================================
tau = R_eq * C
t_analitico_total = np.linspace(a, b, 1000)
V_analitico_total = V0 * np.exp(-t_analitico_total / tau)
U_analitico_total = energia(V_analitico_total)

# Tempo crítico analítico (onde U = U_fogo)
t_critico_analitico = - (tau / 2) * np.log(U_fogo / (0.5 * C * V0**2))

# =====================================================
# RESULTADOS FINAIS
# =====================================================
V_final_num = V_pontos[-1]
U_final_num = U_pontos[-1]
V_final_analitico = V_analitico_total[-1]
U_final_analitico = U_analitico_total[-1]
erro_medio = np.mean(erro_relativo)

# =====================================================
# IMPRESSÃO DOS RESULTADOS
# =====================================================
print("\n==================== RESULTADOS FINAIS ====================")
print(f"Constante de tempo τ = {tau:.4e} s")
print(f"Tempo crítico analítico: {t_critico_analitico:.6f} s")

if tempo_critico is not None:
    print(f"Tempo crítico (RK3): {tempo_critico:.6f} s")
    print(f"Diferença: {abs(tempo_critico - t_critico_analitico):.8f} s")
else:
    print("A energia não atingiu o valor crítico no intervalo de tempo simulado.")

print(f"\nEnergia inicial: {0.5 * C * V0**2:.6f} J")
print(f"Energia final (numérica): {U_final_num:.8e} J")
print(f"Energia final (analítica): {U_final_analitico:.8e} J")

print(f"\nTensão final (numérica): {V_final_num:.6e} V")
print(f"Tensão final (analítica): {V_final_analitico:.6e} V")
print(f"Tensão crítica (para 50 mJ): {np.sqrt(2 * U_fogo / C):.2f} V")

print(f"\nErro relativo médio = {erro_medio:.2e}")
print("============================================================\n")

# =====================================================
# GRÁFICOS
# =====================================================
plt.figure(figsize=(18, 6))

# --- Gráfico da tensão ---
plt.subplot(1, 3, 1)
plt.plot(t_pontos, np.array(V_pontos) / 1000, 'b-', linewidth=2, label='RK3 (Numérico)')
plt.plot(t_analitico_total, V_analitico_total / 1000, 'r--', linewidth=1.5, label='Analítico')
if tempo_critico:
    plt.axvline(x=tempo_critico, color='r', linestyle='--', alpha=0.7, label=f't crítico = {tempo_critico:.2f} s')
plt.xlabel('Tempo (s)')
plt.ylabel('Tensão (kV)')
plt.title('Tensão vs Tempo (Método RK3)')
plt.grid(True)
plt.legend()

# --- Gráfico da energia ---
plt.subplot(1, 3, 2)
plt.plot(t_pontos, np.array(U_pontos) * 1000, 'r-', linewidth=2, label='Energia - RK3 (Numérica)')
plt.plot(t_analitico_total, U_analitico_total * 1000, 'k--', linewidth=1.5, label='Energia - Analítica')
plt.axhline(y=U_fogo * 1000, color='g', linestyle='--', linewidth=1.5, label='U_fogo = 50 mJ')
if tempo_critico:
    plt.axvline(x=tempo_critico, color='r', linestyle='--', alpha=0.7)
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (mJ)')
plt.title('Energia vs Tempo (Método RK3)')
plt.grid(True)
plt.legend()

# --- Gráfico do erro relativo ---
plt.subplot(1, 3, 3)
plt.plot(t_pontos, erro_relativo, color='purple', linewidth=1.5)
plt.title('Erro Relativo do Método RK3')
plt.xlabel('Tempo (s)')
plt.ylabel('Erro relativo')
plt.yscale('log')  # Escala logarítmica para visualizar melhor o erro
plt.grid(True)

plt.tight_layout()
plt.show()