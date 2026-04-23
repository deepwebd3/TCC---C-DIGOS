import numpy as np
import matplotlib.pyplot as plt

# Configuração global para Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

# Definindo a EDO: dy/dx = y - x² + 1
def f(x, y):
    return y - x**2 + 1

# Solução analítica
def solucao_analitica(x):
    return (x + 1)**2 - 0.5 * np.exp(x)

# Parâmetros do método de Euler
x0, y0 = 0.0, 0.5
h = 0.5
x_final = 2.0

# Método de Euler
x_euler = [x0]
y_euler = [y0]
while x_euler[-1] < x_final:
    x_novo = x_euler[-1] + h
    y_novo = y_euler[-1] + h * f(x_euler[-1], y_euler[-1])
    x_euler.append(x_novo)
    y_euler.append(y_novo)

# Solução analítica para comparação
x_analitico = np.linspace(x0, x_final, 200)
y_analitico = solucao_analitica(x_analitico)

# Ajuste de tamanho e proporção (bom para TCC)
plt.figure(figsize=(6, 4))  # ~15,2 cm x 10,1 cm

# Solução analítica
plt.plot(x_analitico, y_analitico, 'b-', label='Solução Analítica', linewidth=1.8)

# Aproximação de Euler
plt.plot(x_euler, y_euler, 'ro--', label='Aproximação de Euler', linewidth=1.2, markersize=5)

# Linhas auxiliares
for i in range(len(x_euler) - 1):
    plt.plot([x_euler[i+1], x_euler[i+1]], [y_euler[i], y_euler[i+1]], 'g--', linewidth=0.6)
    plt.plot([x_euler[i], x_euler[i+1]], [y_euler[i], y_euler[i]], 'g--', linewidth=0.6)
    x_tang = np.linspace(x_euler[i], x_euler[i+1], 10)
    y_tang = y_euler[i] + (x_tang - x_euler[i]) * f(x_euler[i], y_euler[i])
    plt.plot(x_tang, y_tang, 'm:', linewidth=0.6)

# Títulos e rótulos
plt.title('Método de Euler', fontsize=20, pad=15)
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.legend(loc='upper left', prop={'size': 10})

# Anotações
plt.annotate('Passo de integração (h)', xy=(x_euler[0]+h/2, y_euler[0]-0.1), 
             xytext=(x_euler[0]+h/2, y_euler[0]-0.35), fontsize=9)

plt.annotate('Inclinação = f(xₙ, yₙ)', xy=(x_euler[0]+h/4, y_euler[0]+0.1), 
             xytext=(x_euler[0]-0.4, y_euler[0]+0.5), 
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3'), fontsize=9)

plt.annotate('Erro de aproximação', xy=(x_euler[2], y_euler[2]), 
             xytext=(x_euler[2]+0.2, y_euler[2]-0.35), 
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3'), fontsize=9)

# Grade e layout
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# Salvar em alta resolução
plt.savefig('metodo_euler_tcc.png', dpi=600, bbox_inches='tight')
plt.show()