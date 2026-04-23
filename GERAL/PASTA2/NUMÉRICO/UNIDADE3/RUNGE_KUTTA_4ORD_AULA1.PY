import numpy as np
import pylab as plt

# Função que define a equação diferencial: crescimento populacional logístico
def f(P, t):
    return 9.81 - (15/75)*P**2  # Equação logística: dP/dt = rP(1 - P/K)

# Intervalo de tempo da simulação
a = 0                # Tempo inicial
b = 10              # Tempo final
Num = 0.5      # Número de subdivisões (quanto maior, mais preciso)
h = (b - a) / Num    # Tamanho do passo
P = 80                # Condição inicial: população no tempo t=0

# Inicialização dos vetores de tempo e da solução
t_pontos = np.arange(a, b, h)  # Gera os valores de tempo
P_pontos = []                  # Lista para armazenar os valores de P(t)

# Método de Runge-Kutta de 4ª ordem para resolver a EDO
for i in t_pontos:
    P_pontos.append(P)  # Armazena o valor atual de P

    # Cálculo dos coeficientes de Runge-Kutta
    k1 = h * f(P, i)
    k2 = h * f(P + 0.5 * k1, i + 0.5 * h)
    k3 = h * f(P + 0.5 * k2, i + 0.5 * h)
    k4 = h * f(P + k3, i + h)

    # Atualiza o valor de P usando os coeficientes
    P += (k1 + 2 * k2 + 2 * k3 + k4) / 6
    print(f"t = {i:.2f}, P(t) = {P:.4f}")  # Exibe o progresso da simulação
    
    
# Plotagem do resultado
plt.plot(t_pontos, P_pontos, color='#FF4500', linewidth=1.5, label='dP/dt = rP(1 - P/K)')
plt.title('Gráfico da função logística (sigmóide)')  # Título do gráfico
plt.xlabel('t')                                      # Eixo x (tempo)
plt.ylabel('P(t)')                                   # Eixo y (população)
plt.grid(True)                                       # Adiciona a grade
plt.legend()                                         # Mostra a legenda
plt.show()                                           # Exibe o gráfico