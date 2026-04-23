import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do problema
def f(t, y):
    """Exemplo: dy/dt = -y + t (equação linear)"""
    return -y + t

# Solução analítica para dy/dt = -y + t, y(0) = 1
def solucao_analitica(t):
    return t - 1 + 2*np.exp(-t)

# Método de Euler Modificado (Runge-Kutta de 2ª ordem)
def euler_modificado(f, t0, y0, h, n_passos):
    t = np.zeros(n_passos + 1)
    y = np.zeros(n_passos + 1)
    t[0] = t0
    y[0] = y0
    
    # Armazenar pontos intermediários para visualização
    pontos_predicao = []
    pontos_correcao = []
    
    for i in range(n_passos):
        # Predição (Euler simples)
        y_pred = y[i] + h * f(t[i], y[i])
        pontos_predicao.append((t[i] + h, y_pred))
        
        # Correção (Euler modificado)
        y[i+1] = y[i] + h * (f(t[i], y[i]) + f(t[i] + h, y_pred)) / 2
        t[i+1] = t[i] + h
        pontos_correcao.append((t[i+1], y[i+1]))
    
    return t, y, pontos_predicao, pontos_correcao

# Parâmetros da simulação
t0 = 0
y0 = 1
h = 0.5  # Tamanho do passo (grande para visualização)
n_passos = 6
t_final = t0 + n_passos * h

# Executar métodos
t_euler_mod, y_euler_mod, predicoes, correcoes = euler_modificado(f, t0, y0, h, n_passos)

# Solução analítica para comparação
t_analitico = np.linspace(t0, t_final, 1000)
y_analitico = solucao_analitica(t_analitico)

# Método de Euler simples para comparação
def euler_simples(f, t0, y0, h, n_passos):
    t = np.zeros(n_passos + 1)
    y = np.zeros(n_passos + 1)
    t[0] = t0
    y[0] = y0
    
    for i in range(n_passos):
        y[i+1] = y[i] + h * f(t[i], y[i])
        t[i+1] = t[i] + h
    
    return t, y

t_euler, y_euler = euler_simples(f, t0, y0, h, n_passos)

# Criar figura com tamanho reduzido
plt.figure(figsize=(10, 6))

# GRÁFICO PRINCIPAL: Visualização do Método
# Solução analítica
plt.plot(t_analitico, y_analitico, 'b-', linewidth=2, label='Solução Analítica', alpha=0.8)

# Pontos do Euler modificado
plt.plot(t_euler_mod, y_euler_mod, 'ro-', linewidth=1.5, markersize=6, 
         label='Runge-Kutta 2ª Ordem (Pontos Finais)')

# Euler simples para comparação
plt.plot(t_euler, y_euler, 'g--', linewidth=1.2, markersize=4, 
         label='Euler Simples')

# Adicionar setas e pontos intermediários
for i, ((t_pred, y_pred), (t_corr, y_corr)) in enumerate(zip(predicoes, correcoes)):
    # Linha de predição (Euler simples)
    plt.plot([t_euler_mod[i], t_pred], [y_euler_mod[i], y_pred], 'orange', 
             linestyle=':', linewidth=1.5, alpha=0.7, 
             label='Predição Euler' if i == 0 else "")
    
    # Ponto de predição
    plt.plot(t_pred, y_pred, 's', color='orange', markersize=6, 
             label='Ponto Predito' if i == 0 else "")
    
    # Linha de correção
    plt.plot([t_pred, t_corr], [y_pred, y_corr], 'purple', 
             linestyle=':', linewidth=1.5, alpha=0.7,
             label='Correção' if i == 0 else "")
    
    # Setas explicativas (menores)
    plt.arrow(t_euler_mod[i], y_euler_mod[i], h, h*f(t_euler_mod[i], y_euler_mod[i]), 
              head_width=0.03, head_length=0.03, fc='orange', ec='orange', alpha=0.6)
    
    plt.arrow(t_pred, y_pred, 0, y_corr - y_pred, 
              head_width=0.02, head_length=0.02, fc='purple', ec='purple', alpha=0.6)

plt.xlabel('t', fontsize=10)
plt.ylabel('y(t)', fontsize=10)
plt.title('', fontsize=11)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=9)
plt.ylim(0.5, 1.8)

# Layout mais compacto
plt.tight_layout(pad=1.0)

plt.show()