import numpy as np
import matplotlib.pyplot as plt

# Função que define a equação diferencial: dv/dt = g - (c/m)v²
def f(v, t):
    return 9.81 - (15/75) * v**2

# Solução analítica
def solucao_analitica(t):
    g = 9.81
    c = 15
    m = 75
    return np.sqrt(m*g/c) * np.tanh(np.sqrt(g*c/m) * t)

# Parâmetros da simulação
a = 0                # Tempo inicial (s)
b = 10               # Tempo final (s)
h = 0.5              # Tamanho do passo (s)
v0 = 0               # Condição inicial: velocidade no tempo t=0 (m/s)

# Cálculo do número de passos
Num = int((b - a) / h)

# Inicialização dos vetores
t_pontos = np.arange(a, b + h, h)  # Gera os valores de tempo (incluindo t=10)
v_pontos = []                      # Lista para valores numéricos
v_analitica = []                   # Lista para valores analíticos

# Método de Runge-Kutta de 4ª ordem
v = v0
for t in t_pontos:
    v_pontos.append(v)
    v_analitica.append(solucao_analitica(t))
    
    # Cálculo dos coeficientes RK4
    k1 = h * f(v, t)
    k2 = h * f(v + 0.5 * k1, t + 0.5 * h)
    k3 = h * f(v + 0.5 * k2, t + 0.5 * h)
    k4 = h * f(v + k3, t + h)
    
    v += (k1 + 2*k2 + 2*k3 + k4) / 6
    print(f"t = {t:.2f} s | v_num = {v_pontos[-1]:.6f} m/s | v_ana = {v_analitica[-1]:.6f} m/s")

# Cálculo da velocidade terminal
v_terminal = np.sqrt(9.81 * 75 / 15)

# Cálculo do erro absoluto em t = 10s
erro_absoluto = abs(v_pontos[-1] - v_analitica[-1])
print(f"\nVelocidade terminal teórica: {v_terminal:.6f} m/s")
print(f"Erro absoluto em t=10s: {erro_absoluto:.6f} m/s")

# Plotagem
plt.figure(figsize=(12, 6))
plt.plot(t_pontos, v_pontos, 'r-', linewidth=2, label='Solução Numérica (RK4)')
plt.plot(t_pontos, v_analitica, 'b--', linewidth=1.5, label='Solução Analítica')
plt.axhline(y=v_terminal, color='g', linestyle=':', label='Velocidade Terminal')

plt.title('Queda com Resistência do Ar - Comparação Numérico vs Analítico')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.grid(True)
plt.legend()
plt.show()