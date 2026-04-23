import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# PARÂMETROS DO PROBLEMA
# =====================================================
V0 = 30e3        # 30 kV
C = 500e-12      # 500 pF
R_pneu = 100e9   # 100 GΩ
U_fogo = 50e-3   # 50 mJ

# Resistência equivalente (4 pneus em paralelo)
R_eq = R_pneu / 4

# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================
def f(V, t):
    """Equação diferencial: dV/dt = -V / (R_eq * C)"""
    return -V / (R_eq * C)

def solucao_analitica(t):
    """Solução analítica: V(t) = V0 * exp(-t / (R_eq * C))"""
    return V0 * np.exp(-t / (R_eq * C))

def energia(V):
    """Energia armazenada: U = (1/2)*C*V²"""
    return 0.5 * C * V**2

# =====================================================
# PARÂMETROS DE SIMULAÇÃO
# =====================================================
a = 0
b = 10
Num = 1000
h = (b - a) / Num

V = V0
U = energia(V)

t_pontos = np.arange(a, b, h)
V_pontos, U_pontos, erro_relativo_pontos = [], [], []
t_critico = None

# =====================================================
# MÉTODO DE RUNGE-KUTTA DE 4ª ORDEM (RK4)
# =====================================================
for t in t_pontos:
    V_pontos.append(V)
    U = energia(V)
    U_pontos.append(U)

    # Solução analítica e erro relativo
    V_analitico = solucao_analitica(t)
    erro_relativo = abs(V - V_analitico) / abs(V_analitico)
    erro_relativo_pontos.append(erro_relativo)

    # Verifica energia crítica
    if U <= U_fogo and t_critico is None:
        t_critico = t
        print("\n=== TEMPO CRÍTICO ALCANÇADO (NUMÉRICO) ===")
        print(f"t = {t:.6f} s")
        print(f"Tensão numérica:   {V:.6e} V")
        print(f"Tensão analítica:  {V_analitico:.6e} V")
        print(f"Energia numérica:  {U:.8e} J")

    # Coeficientes RK4
    k1 = h * f(V, t)
    k2 = h * f(V + 0.5 * k1, t + 0.5 * h)
    k3 = h * f(V + 0.5 * k2, t + 0.5 * h)
    k4 = h * f(V + k3, t + h)

    # Atualiza V
    V += (k1 + 2*k2 + 2*k3 + k4) / 6

# =====================================================
# ANÁLISE DE ERROS
# =====================================================
erro_maximo = np.max(erro_relativo_pontos)
erro_medio = np.mean(erro_relativo_pontos)

# =====================================================
# RESULTADOS FINAIS
# =====================================================
tau = R_eq * C
t_critico_analitico = - (tau / 2) * np.log(U_fogo / (0.5 * C * V0**2))

print("\n" + "="*60)
print("RESULTADOS DA SIMULAÇÃO (MÉTODO RK4)")
print("="*60)
print(f"Constante de tempo τ = {tau:.4e} s")
print(f"Tensão inicial:      {V0/1000:.2f} kV")
print(f"Energia inicial:     {0.5*C*V0**2*1000:.4f} mJ")
print(f"Energia crítica:     {U_fogo*1000:.2f} mJ")
print(f"Resistência eq.:     {R_eq/1e9:.2f} GΩ")

if t_critico is not None:
    erro_tempo = abs(t_critico - t_critico_analitico)
    print(f"\nTempo crítico (numérico):   {t_critico:.6f} s")
    print(f"Tempo crítico (analítico):  {t_critico_analitico:.6f} s")
    print(f"Desvio absoluto:            {erro_tempo:.3e} s")
else:
    print("\n⚠️ A energia não atingiu o valor crítico no tempo simulado.")
    print(f"Energia final após {b:.1f} s: {U_pontos[-1]*1000:.6f} mJ")

print(f"\nErro máximo relativo: {erro_maximo:.2e}")
print(f"Erro médio relativo:  {erro_medio:.2e}")
print("="*60)

# =====================================================
# PLOTS
# =====================================================
plt.figure(figsize=(16, 8))

# --- Tensão ---
plt.subplot(2, 2, 1)
plt.plot(t_pontos, np.array(V_pontos)/1000, color='blue', linewidth=2, label='RK4 (Numérico)')
plt.plot(t_pontos, solucao_analitica(t_pontos)/1000, 'r--', linewidth=1.5, label='Analítico')
plt.axhline(y=np.sqrt(2*U_fogo/C)/1000, color='red', linestyle=':', label='Tensão crítica')
if t_critico:
    plt.axvline(x=t_critico, color='orange', linestyle='--', label=f't crítico = {t_critico:.2f}s')
plt.title('Tensão vs Tempo (Método RK4)')
plt.xlabel('Tempo (s)')
plt.ylabel('Tensão (kV)')
plt.grid(True)
plt.legend()

# --- Energia ---
plt.subplot(2, 2, 2)
plt.plot(t_pontos, np.array(U_pontos)*1000, color='darkred', linewidth=2, label='RK4 (Numérica)')
plt.plot(t_pontos, energia(solucao_analitica(t_pontos))*1000, 'k--', linewidth=1.5, label='Analítica')
plt.axhline(y=U_fogo*1000, color='green', linestyle=':', label='Energia crítica (50 mJ)')
if t_critico:
    plt.axvline(x=t_critico, color='orange', linestyle='--', alpha=0.7)
plt.title('Energia vs Tempo (Método RK4)')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (mJ)')
plt.grid(True)
plt.legend()

# --- Erro relativo ---
plt.subplot(2, 2, 3)
plt.plot(t_pontos, erro_relativo_pontos, color='purple', linewidth=1.5)
plt.title('Erro Relativo do Método RK4')
plt.xlabel('Tempo (s)')
plt.ylabel('Erro relativo')
plt.yscale('log')
plt.grid(True)

plt.tight_layout()
plt.show()