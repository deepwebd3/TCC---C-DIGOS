import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do modelo
kgm = 0.026         # taxa de crescimento
pmax = 12000        # capacidade máxima (milhões de pessoas)
p0 = 2555           # população inicial em 1950 (milhões)
t0 = 1950           # ano inicial
tf = 2000           # ano final
dt = 1              # passo em anos

# Vetores para armazenar resultados
t = np.arange(t0, tf + 1, dt)
p = np.zeros(len(t))
p[0] = p0

# Método de Euler
for i in range(1, len(t)):
    dpdt = kgm * (1 - p[i-1]/pmax) * p[i-1]
    p[i] = p[i-1] + dpdt * dt

# Dados reais fornecidos
t_real = np.array([1950, 1960, 1970, 1980, 1990, 2000])
p_real = np.array([2.555, 3.040, 3.708, 4.454, 5.276, 6.079]) * 1e3  # converter milhões para mil

print("Dados reais (milhões):", p_real)

# Gráfico comparativo
plt.figure(figsize=(10, 6))
plt.plot(t, p, label='Simulação (Modelo Logístico)', color='blue')
plt.plot(t_real, p_real, 'ro', label='Dados Reais')
plt.xlabel('Ano')
plt.ylabel('População (milhões)')  
plt.title('Crescimento da População Mundial (1950-2000)')
plt.legend()
plt.grid(True)
plt.show()