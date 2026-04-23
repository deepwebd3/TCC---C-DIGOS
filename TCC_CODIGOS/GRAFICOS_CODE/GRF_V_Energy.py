import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do problema
U_fogo = 50e-3  # 50 mJ (energia crítica)
V0 = 30e3       # 30 kV (tensão inicial)
C = 500e-12     # 500 pF (capacitância)
R_pneu = 100e9  # 100 GΩ (resistência por pneu)

# Como o carro tem 4 pneus em paralelo, a resistência equivalente é R_pneu/4
R_eq = R_pneu / 4

# A energia no capacitor é U = (1/2) * C * V²
# Queremos encontrar quando U(t) = U_fogo

# A tensão no capacitor descarregando segue: V(t) = V0 * exp(-t/(R_eq*C))
# Portanto: (1/2) * C * [V0 * exp(-t/(R_eq*C))]² = U_fogo

# Equação diferencial: dV/dt = -V/(R_eq*C)
def f(V, t):
    return -V / (R_eq * C)

# Função para calcular a energia
def energia(V):
    return 0.5 * C * V**2

# Intervalo de tempo da simulação (vamos estimar um tempo razoável)
a = 0                # Tempo inicial
b = 100             # Tempo final em segundos
Num = 1000          # Número de subdivisões
h = (b - a) / Num    # Tamanho do passo
V = V0              # Condição inicial: tensão no tempo t=0

# Inicialização dos vetores
t_pontos = np.arange(a, b, h)
V_pontos = []
U_pontos = []

# Método de Runge-Kutta de 4ª ordem
for i in t_pontos:
    V_pontos.append(V)
    U = energia(V)
    U_pontos.append(U)
    
    # Se a energia caiu abaixo do valor crítico, podemos parar
    if U <= U_fogo:
        
        break
    
    # Cálculo dos coeficientes RK4
    k1 = h * f(V, i)
    k2 = h * f(V + 0.5 * k1, i + 0.5 * h)
    k3 = h * f(V + 0.5 * k2, i + 0.5 * h)
    k4 = h * f(V + k3, i + h)
    
    V += (k1 + 2 * k2 + 2 * k3 + k4) / 6

# Solução analítica para comparação
# Tempo analítico: t = -R_eq*C * ln(sqrt(2*U_fogo/(C*V0²)))
t_analitico = -R_eq * C * np.log(np.sqrt(2 * U_fogo / (C * V0**2)))


# Plotagem dos resultados
plt.figure(figsize=(10, 5))

# Gráfico da tensão
plt.subplot(1, 2, 1)
plt.plot(t_pontos[:len(V_pontos)], np.array(V_pontos)/1000, 'b-', linewidth=2, label='Tensão V(t)')
plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
plt.xlabel('Tempo (s)')
plt.ylabel('Tensão (kV)')
plt.title('')
plt.grid(True)
plt.legend()

# Gráfico da energia
plt.subplot(1, 2, 2)
plt.plot(t_pontos[:len(U_pontos)], np.array(U_pontos)*1000, 'r-', linewidth=2, label='Energia U(t)')
plt.axhline(y=U_fogo*1000, color='g', linestyle='--', label='U_fogo = 50 mJ')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (mJ)')
plt.title('')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
print(f'Tempo para a energia atingir {U_fogo*1000:.1f} mJ (simulação numérica): {t_pontos[len(U_pontos)-1]:.4f} s')
print(f'Tempo para a energia atingir {U_fogo*1000:.1f} mJ (solução analítica): {t_analitico:.4f} s')
print(f' Tensão final no tempo crítico: {V_pontos[-1]/1000:.4f} kV')
print(f' Energia final no tempo crítico: {U_pontos[-1]*1000:.4f} mJ')