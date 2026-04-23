import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do modelo
N = 1000             # População total
I0, R0 = 1, 0        # Infectados e recuperados iniciais
S0 = N - I0 - R0     # Suscetíveis iniciais
beta = 0.2           # Taxa de contato (transmissão)
gamma = 1 / 10       # Taxa de recuperação (1/dias de recuperação)

# Intervalo de tempo (de 0 a 160 dias, 160 pontos)
t = np.linspace(0, 160, 160)
dt = t[1] - t[0]     # Passo de tempo
n = len(t)           # Número total de pontos no tempo

# Inicialização dos vetores que armazenarão os resultados
S = np.zeros(n)      # Vetor para suscetíveis
I = np.zeros(n)      # Vetor para infectados
R = np.zeros(n)      # Vetor para recuperados

# Condições iniciais no tempo t=0
S[0] = S0
I[0] = I0
R[0] = R0

# Função que calcula as derivadas (modelo SIR)
def deriv(s, i, r, beta, gamma, N):
    dSdt = -beta * s * i / N             # Variação dos suscetíveis
    dIdt = beta * s * i / N - gamma * i  # Variação dos infectados
    dRdt = gamma * i                     # Variação dos recuperados
    return dSdt, dIdt, dRdt

# Método de Runge-Kutta de 4ª ordem para resolver o sistema
for k in range(n - 1):
    # Cálculo dos coeficientes de Runge-Kutta
    k1_S, k1_I, k1_R = deriv(S[k], I[k], R[k], beta, gamma, N)
    k2_S, k2_I, k2_R = deriv(S[k] + dt * k1_S / 2, I[k] + dt * k1_I / 2, R[k] + dt * k1_R / 2, beta, gamma, N)
    k3_S, k3_I, k3_R = deriv(S[k] + dt * k2_S / 2, I[k] + dt * k2_I / 2, R[k] + dt * k2_R / 2, beta, gamma, N)
    k4_S, k4_I, k4_R = deriv(S[k] + dt * k3_S,     I[k] + dt * k3_I,     R[k] + dt * k3_R,     beta, gamma, N)

    # Atualização dos valores de S, I, R
    S[k+1] = S[k] + (dt / 6) * (k1_S + 2 * k2_S + 2 * k3_S + k4_S)
    I[k+1] = I[k] + (dt / 6) * (k1_I + 2 * k2_I + 2 * k3_I + k4_I)
    R[k+1] = R[k] + (dt / 6) * (k1_R + 2 * k2_R + 2 * k3_R + k4_R)

# Plotagem dos resultados
plt.figure(figsize=(5, 5))
plt.plot(t, S / N, 'b', label='Suscetíveis')   # Proporção de suscetíveis (azul)
plt.plot(t, I / N, 'r', label='Infectados')    # Proporção de infectados (vermelho)
plt.plot(t, R / N, 'g', label='Recuperados')   # Proporção de recuperados (verde)
plt.title('Modelo SIR com Runge-Kutta de 4ª Ordem')
plt.xlabel('Tempo (dias)')
plt.ylabel('Proporção da População')
plt.ylim(0, 1.2)
plt.grid(True)
plt.legend()
plt.show()