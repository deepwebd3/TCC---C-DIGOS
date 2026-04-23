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

# Criar figura
plt.figure(figsize=(14, 10))

# =============================================
# GRÁFICO PRINCIPAL: Visualização do Método
# =============================================

plt.subplot(2, 2, 1)
# Solução analítica
plt.plot(t_analitico, y_analitico, 'b-', linewidth=3, label='Solução Analítica', alpha=0.8)

# Pontos do Euler modificado
plt.plot(t_euler_mod, y_euler_mod, 'ro-', linewidth=2, markersize=8, 
         label='Euler Modificado (Pontos Finais)')

# Euler simples para comparação
plt.plot(t_euler, y_euler, 'g--', linewidth=1.5, markersize=6, 
         label='Euler Simples')

# Adicionar setas e pontos intermediários
for i, ((t_pred, y_pred), (t_corr, y_corr)) in enumerate(zip(predicoes, correcoes)):
    # Linha de predição (Euler simples)
    plt.plot([t_euler_mod[i], t_pred], [y_euler_mod[i], y_pred], 'orange', 
             linestyle=':', linewidth=2, alpha=0.7, 
             label='Predição Euler' if i == 0 else "")
    
    # Ponto de predição
    plt.plot(t_pred, y_pred, 's', color='orange', markersize=8, 
             label='Ponto Predito' if i == 0 else "")
    
    # Linha de correção
    plt.plot([t_pred, t_corr], [y_pred, y_corr], 'purple', 
             linestyle=':', linewidth=2, alpha=0.7,
             label='Correção' if i == 0 else "")
    
    # Setas explicativas
    plt.arrow(t_euler_mod[i], y_euler_mod[i], h, h*f(t_euler_mod[i], y_euler_mod[i]), 
              head_width=0.05, head_length=0.05, fc='orange', ec='orange', alpha=0.6)
    
    plt.arrow(t_pred, y_pred, 0, y_corr - y_pred, 
              head_width=0.03, head_length=0.03, fc='purple', ec='purple', alpha=0.6)

plt.xlabel('t')
plt.ylabel('y(t)')
plt.title('Método de Euler Modificado (RK2) - Visualização Detalhada')
plt.grid(True, alpha=0.3)
plt.legend()
plt.ylim(0.5, 1.8)

# =============================================
# GRÁFICO 2: Comparação de Erros
# =============================================

plt.subplot(2, 2, 2)
# Calcular soluções com passo menor para análise de erro
h_pequeno = 0.1
n_pequeno = int((t_final - t0) / h_pequeno)

t_euler_peq, y_euler_peq = euler_simples(f, t0, y0, h_pequeno, n_pequeno)
t_mod_peq, y_mod_peq, _, _ = euler_modificado(f, t0, y0, h_pequeno, n_pequeno)

# Calcular erros
erro_euler = np.abs(y_euler_peq - solucao_analitica(t_euler_peq))
erro_modificado = np.abs(y_mod_peq - solucao_analitica(t_mod_peq))

plt.semilogy(t_euler_peq, erro_euler, 'g-', linewidth=2, label='Erro Euler Simples')
plt.semilogy(t_mod_peq, erro_modificado, 'r-', linewidth=2, label='Erro Euler Modificado')
plt.xlabel('t')
plt.ylabel('Erro Absoluto (escala log)')
plt.title('Comparação de Erros: Euler vs Euler Modificado')
plt.grid(True, alpha=0.3)
plt.legend()

# =============================================
# GRÁFICO 3: Diagrama de Fluxo do Método
# =============================================

plt.subplot(2, 2, 3)
# Criar um diagrama esquemático
etapas = ['yₙ', 'Predição\nk₁ = h·f(tₙ,yₙ)\nyᵖ = yₙ + k₁', 
          'Correção\nk₂ = h·f(tₙ₊₁,yᵖ)\nyₙ₊₁ = yₙ + (k₁+k₂)/2', 'yₙ₊₁']

x_pos = [0, 1, 2, 3]
y_pos = [0, 0, 0, 0]

# Plotar caixas
caixas = []
for i, (etapa, x, y) in enumerate(zip(etapas, x_pos, y_pos)):
    caixa = plt.Rectangle((x-0.4, y-0.2), 0.8, 0.4, fill=True, 
                         facecolor='lightblue' if i % 2 == 0 else 'lightgreen',
                         edgecolor='black', linewidth=2)
    plt.gca().add_patch(caixa)
    plt.text(x, y, etapa, ha='center', va='center', fontweight='bold')

# Setas
plt.arrow(0.4, 0, 0.2, 0, head_width=0.05, head_length=0.1, fc='black')
plt.arrow(1.4, 0, 0.2, 0, head_width=0.05, head_length=0.1, fc='black')
plt.arrow(2.4, 0, 0.2, 0, head_width=0.05, head_length=0.1, fc='black')

plt.text(0.5, 0.3, 'Passo 1', ha='center', fontsize=10)
plt.text(1.5, 0.3, 'Passo 2', ha='center', fontsize=10)
plt.text(2.5, 0.3, 'Passo 3', ha='center', fontsize=10)

plt.xlim(-0.5, 3.5)
plt.ylim(-0.5, 0.5)
plt.axis('off')
plt.title('Diagrama do Método de Euler Modificado')

# =============================================
# GRÁFICO 4: Influência do Tamanho do Passo
# =============================================

plt.subplot(2, 2, 4)
tamanhos_passo = [0.8, 0.5, 0.2, 0.1]
cores = ['red', 'blue', 'green', 'purple']

for i, h_test in enumerate(tamanhos_passo):
    n_test = int((t_final - t0) / h_test)
    t_test, y_test, _, _ = euler_modificado(f, t0, y0, h_test, n_test)
    
    # Calcular erro máximo
    erro_max = np.max(np.abs(y_test - solucao_analitica(t_test)))
    
    plt.plot(h_test, erro_max, 'o', color=cores[i], markersize=10,
             label=f'h = {h_test}, Erro = {erro_max:.4f}')

# Linha teórica (erro ∝ h²)
h_teorico = np.linspace(0.1, 0.8, 50)
erro_teorico = 0.1 * h_teorico**2  # Erro O(h²)
plt.plot(h_teorico, erro_teorico, 'k--', label='O(h²) - Erro teórico')

plt.xlabel('Tamanho do Passo (h)')
plt.ylabel('Erro Máximo')
plt.title('Influência do Tamanho do Passo no Erro')
plt.grid(True, alpha=0.3)
plt.legend()
plt.yscale('log')

# =============================================
# TEXTO EXPLICATIVO
# =============================================

plt.figtext(0.02, 0.02, 
"""
MÉTODO DE EULER MODIFICADO (Runge-Kutta de 2ª Ordem):

1. PREDIÇÃO (Euler Simples):
   yᵖ = yₙ + h·f(tₙ, yₙ)

2. CORREÇÃO (Média das Derivadas):
   yₙ₊₁ = yₙ + h·[f(tₙ, yₙ) + f(tₙ₊₁, yᵖ)]/2

Vantagens sobre Euler Simples:
• Erro de truncamento: O(h²) vs O(h) do Euler simples
• Maior precisão com mesmo tamanho de passo
• Estabilidade numérica melhorada
""", 
bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"), fontsize=10)

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.show()

# =============================================
# ESTATÍSTICAS NUMÉRICAS
# =============================================

print(f"\n=== COMPARAÇÃO DE MÉTODOS (h = {h}) ===")
print(f"{'Método':<20} {'Erro Máximo':<12} {'Ordem do Erro':<15}")
print("-" * 50)

erro_max_euler = np.max(np.abs(y_euler - solucao_analitica(t_euler)))
erro_max_modificado = np.max(np.abs(y_euler_mod - solucao_analitica(t_euler_mod)))

print(f"{'Euler Simples':<20} {erro_max_euler:<12.6f} O(h)")
print(f"{'Euler Modificado':<20} {erro_max_modificado:<12.6f} O(h²)")
print(f"{'Melhoria':<20} {erro_max_euler/erro_max_modificado:<12.2f}x")