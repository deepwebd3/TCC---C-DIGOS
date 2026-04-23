import numpy as np
import matplotlib.pyplot as plt

# Configurações globais de fonte
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 16  # Tamanho base aumentado
plt.rcParams['axes.titlesize'] = 18  # Título do gráfico
plt.rcParams['axes.labelsize'] = 16  # Rótulos dos eixos
plt.rcParams['xtick.labelsize'] = 16  # Rótulos do eixo x
plt.rcParams['ytick.labelsize'] = 16  # Rótulos do eixo y
plt.rcParams['legend.fontsize'] = 14  # Legenda

# Definindo a EDO: dy/dx = f(x, y)
def f(x, y):
    return y - x**2 + 1  # Exemplo: dy/dx = y - x² + 1

# Solução analítica para comparação
def solucao_analitica(x):
    return (x + 1)**2 - 0.5 * np.exp(x)

# Parâmetros do método
x0 = 0.0
y0 = 0.5
h = 0.5  # Tamanho do passo
x_final = 2.0

# Método de Heun (preditor-corretor)
x_heun = [x0]
y_preditor = [y0]  # Armazena as previsões (Euler)
y_heun = [y0]      # Armazena as correções (Heun)

# Executando o método de Heun
while x_heun[-1] < x_final:
    # **Etapa Preditora (Euler)**
    x_novo = x_heun[-1] + h
    y_pred = y_heun[-1] + h * f(x_heun[-1], y_heun[-1])
    
    # **Etapa Corretora (Heun)**
    y_corr = y_heun[-1] + (h / 2) * (f(x_heun[-1], y_heun[-1]) + f(x_novo, y_pred))
    
    # Armazenando valores
    x_heun.append(x_novo)
    y_preditor.append(y_pred)
    y_heun.append(y_corr)

# Gerando pontos para a solução analítica
x_analitico = np.linspace(x0, x_final, 100)
y_analitico = solucao_analitica(x_analitico)

# Criando o gráfico focado na **etapa corretora**
plt.figure(figsize=(14, 8))  # Tamanho ligeiramente aumentado

# 1. Solução analítica (referência)
plt.plot(x_analitico, y_analitico, 'b-', label='Solução Analítica', linewidth=2.5)

# 2. Previsão de Euler (Preditor)
plt.plot(x_heun, y_preditor, 'ro--', label='Previsão (Euler)', linewidth=1.5, markersize=9, alpha=0.7)

# 3. Solução corrigida (Heun)
plt.plot(x_heun, y_heun, 'go-', label='Correção (Heun)', linewidth=2.5, markersize=9)

# 4. Elementos explicativos da **correção**
for i in range(len(x_heun) - 1):
    # Ponto inicial (verde)
    plt.scatter(x_heun[i], y_heun[i], color='green', s=120, zorder=5)
    
    # Previsão de Euler (vermelho)
    plt.scatter(x_heun[i+1], y_preditor[i+1], color='red', s=120, zorder=5)
    
    # Correção de Heun (verde)
    plt.scatter(x_heun[i+1], y_heun[i+1], color='lime', s=120, zorder=5, edgecolor='black')
    
    # Inclinação no ponto inicial (f(xₙ, yₙ))
    x_tang1 = np.linspace(x_heun[i], x_heun[i+1], 10)
    y_tang1 = y_heun[i] + (x_tang1 - x_heun[i]) * f(x_heun[i], y_heun[i])
    plt.plot(x_tang1, y_tang1, 'm:', linewidth=2, label='Inclinação em (xₙ,yₙ)' if i == 0 else "")
    
    # Inclinação no ponto predito (f(xₙ₊₁, yₙ₊₁_pred)))
    x_tang2 = np.linspace(x_heun[i], x_heun[i+1], 10)
    y_tang2 = y_heun[i] + (x_tang2 - x_heun[i]) * f(x_heun[i+1], y_preditor[i+1])
    plt.plot(x_tang2, y_tang2, 'c:', linewidth=2, label='Inclinação em (xₙ₊₁,yₙ₊₁_pred)' if i == 0 else "")
    
    # Média das inclinações (etapa corretora)
    x_tang_avg = np.linspace(x_heun[i], x_heun[i+1], 10)
    y_tang_avg = y_heun[i] + (x_tang_avg - x_heun[i]) * 0.5 * (f(x_heun[i], y_heun[i]) + f(x_heun[i+1], y_preditor[i+1]))
    plt.plot(x_tang_avg, y_tang_avg, 'k-', linewidth=2.5, label='Inclinação média (Heun)' if i == 0 else "")

# Anotações explicativas
plt.annotate('Previsão (Euler)',
             xy=(x_heun[1], y_preditor[1]),
             xytext=(x_heun[1]-0.4, y_preditor[1]+0.4),
             arrowprops=dict(arrowstyle='->', linewidth=1.5),
             bbox=dict(boxstyle='round,pad=0.6', fc='white', alpha=0.9),
             fontsize=20)

plt.annotate('Correção (Heun)',
             xy=(x_heun[1], y_heun[1]),
             xytext=(x_heun[1]+0.3, y_heun[1]-0.4),
             arrowprops=dict(arrowstyle='->', linewidth=1.5),
             bbox=dict(boxstyle='round,pad=0.6', fc='white', alpha=0.9),
             fontsize=20)

plt.annotate('Inclinação média\n(usada na correção)',
             xy=(x_heun[0]+h/2, y_heun[0] + 0.25),
             xytext=(x_heun[0]-0.6, y_heun[0]+0.6),
             arrowprops=dict(arrowstyle='->', linewidth=1.5),
             fontsize=20,
             ha='center')

# Configurações do gráfico (COM A JUSTE DA LEGENDA)
plt.title('Método de Heun - Etapa Corretora', pad=25, fontsize=30)
plt.xlabel('x')
plt.ylabel('y')
plt.legend(
    loc='upper left',
    framealpha=0.95,
    prop={'family': 'Times New Roman', 'size': 18}  # Tamanho aumentado para as legendas
)
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()