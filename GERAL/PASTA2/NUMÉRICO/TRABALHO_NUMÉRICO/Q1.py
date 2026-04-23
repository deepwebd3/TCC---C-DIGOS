import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do modelo
kgm = 0.026         # taxa de crescimento
pmax = 12000        # capacidade máxima (milhões)
p0 = 2555           # população inicial em 1950 (milhões)
t0 = 1950
tf = 2000
dt = 1

# Vetores para armazenar resultados
t = np.arange(t0, tf + 1, dt)
p = np.zeros(len(t))
p[0] = p0

# Método de Euler para simulação
for i in range(1, len(t)):
    dpdt = kgm * (1 - p[i-1]/pmax) * p[i-1]
    p[i] = p[i-1] + dpdt * dt

# Função para obter valores simulados em anos específicos
def obter_valores_simulados(anos_consultados, t_simulado, p_simulado):
    anos_consultados = np.array(anos_consultados)
    indices = anos_consultados - t_simulado[0]
    return p_simulado[indices]

# Anos e dados reais
t_real = np.array([1950, 1960, 1970, 1980, 1990, 2000])
p_real = np.array([2.555, 3.040, 3.708, 4.454, 5.276, 6.079]) * 1e3  # converter para mil

# Obter valores simulados nos anos reais
p_simulado_nos_anos = obter_valores_simulados(t_real, t, p)

# Mostrar resultados
print("Ano   | População Real (milhões) | População Simulada (milhões)")
for ano, real, sim in zip(t_real, p_real, p_simulado_nos_anos):
    print(f"{ano} | {real:.3f}                   | {sim:.3f}")

# Gráfico comparativo
plt.figure(figsize=(10, 6))
plt.plot(t, p, label='Simulação (Modelo Logístico)', color='blue')
plt.plot(t_real, p_real, 'ro', label='Dados Reais')
plt.plot(t_real, p_simulado_nos_anos, 'gx', label='Simulado nos Anos Reais')
plt.xlabel('Ano')
plt.ylabel('População (milhões)')
plt.title('Crescimento da População Mundial (1950–2000)')
plt.legend()
plt.grid(True)
plt.show()