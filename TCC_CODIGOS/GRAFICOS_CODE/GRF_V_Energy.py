import os
import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do problema
U_fogo = 50e-3  # 50 mJ (energia crítica)
V0 = 30e3       # 30 kV (tensão inicial)
C = 500e-12     # 500 pF (capacitância)
R_pneu = 100e9  # 100 GΩ (resistência por pneu)

# Como o carro tem 4 pneus em paralelo, a resistência equivalente é R_pneu/4
R_eq = R_pneu / 4

# Equação diferencial: dV/dt = -V/(R_eq*C)
def f(V, t):
    return -V / (R_eq * C)

# Função para calcular a energia
def energia(V):
    return 0.5 * C * V**2

# Intervalo de tempo da simulação
a = 0
b = 100
Num = 1000
h = (b - a) / Num
V = V0

# Inicialização dos vetores
t_pontos = np.arange(a, b, h)
V_pontos = []
U_pontos = []

# Método de Runge-Kutta de 4ª ordem
for i in t_pontos:
    V_pontos.append(V)
    U = energia(V)
    U_pontos.append(U)

    if U <= U_fogo:
        break

    k1 = h * f(V, i)
    k2 = h * f(V + 0.5 * k1, i + 0.5 * h)
    k3 = h * f(V + 0.5 * k2, i + 0.5 * h)
    k4 = h * f(V + k3, i + h)

    V += (k1 + 2 * k2 + 2 * k3 + k4) / 6

# Solução analítica para comparação
t_analitico = -R_eq * C * np.log(np.sqrt(2 * U_fogo / (C * V0**2)))

# ===========================================
# CAMINHO DE SAÍDA
# ===========================================
pasta_base = os.path.dirname(os.path.dirname(__file__))
pasta_saida = os.path.join(pasta_base, "GRAFICOS_PNG")
os.makedirs(pasta_saida, exist_ok=True)
arquivo_saida = os.path.join(pasta_saida, "tensao_energia.png")

# Plotagem dos resultados
plt.figure(figsize=(10, 5))

# Gráfico da tensão
plt.subplot(1, 2, 1)
plt.plot(t_pontos[:len(V_pontos)], np.array(V_pontos) / 1000, 'b-', linewidth=2, label='Tensão V(t)')
plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
plt.xlabel('Tempo (s)')
plt.ylabel('Tensão (kV)')
plt.title('')
plt.grid(True)
plt.legend()

# Gráfico da energia
plt.subplot(1, 2, 2)
plt.plot(t_pontos[:len(U_pontos)], np.array(U_pontos) * 1000, 'r-', linewidth=2, label='Energia U(t)')
plt.axhline(y=U_fogo * 1000, color='g', linestyle='--', label='U_fogo = 50 mJ')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (mJ)')
plt.title('')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig(arquivo_saida, dpi=300, bbox_inches="tight")
plt.show()
plt.close()

print(f'Tempo para a energia atingir {U_fogo*1000:.1f} mJ (simulação numérica): {t_pontos[len(U_pontos)-1]:.4f} s')
print(f'Tempo para a energia atingir {U_fogo*1000:.1f} mJ (solução analítica): {t_analitico:.4f} s')
print(f'Tensão final no tempo crítico: {V_pontos[-1]/1000:.4f} kV')
print(f'Energia final no tempo crítico: {U_pontos[-1]*1000:.4f} mJ')