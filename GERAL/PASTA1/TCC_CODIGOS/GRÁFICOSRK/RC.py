import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

# Configuração do estilo visual
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.5

# Parâmetros do circuito RC
R = 1000  # Resistência em Ohms
C = 100e-6  # Capacitância em Farads (100 μF)
V_fonte = 5  # Tensão da fonte em Volts
tau = R * C  # Constante de tempo RC

# Tempo de simulação (até 5 constantes de tempo)
t = np.linspace(0, 5*tau, 1000)

# Equações do circuito RC
V_capacitor = V_fonte * (1 - np.exp(-t/tau))  # Tensão no capacitor
I_circuito = (V_fonte/R) * np.exp(-t/tau)     # Corrente no circuito
V_resistor = V_fonte * np.exp(-t/tau)         # Tensão no resistor

# Criando a figura com subplots
fig = plt.figure(figsize=(15, 10))
grid = plt.GridSpec(3, 2, width_ratios=[1, 1], height_ratios=[1, 1, 1], hspace=0.4, wspace=0.3)

# Axes para o circuito
ax_circuito = fig.add_subplot(grid[0, 0])
ax_graficos = fig.add_subplot(grid[0, 1])
ax_tensao = fig.add_subplot(grid[1, :])
ax_corrente = fig.add_subplot(grid[2, :])

# Configuração dos axes
ax_circuito.set_xlim(0, 10)
ax_circuito.set_ylim(0, 10)
ax_circuito.set_aspect('equal')
ax_circuito.axis('off')
ax_circuito.set_title('Representação do Circuito RC', pad=20, fontsize=14, fontweight='bold')

# Desenhar o circuito RC
def draw_circuit(ax, V_c, I):
    # Limpar o axes
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Representação do Circuito RC', pad=20, fontsize=14, fontweight='bold')
    
    # Fonte de tensão
    ax.add_patch(patches.Rectangle((1, 3), 2, 4, fill=True, color='lightblue', ec='black', lw=2))
    ax.plot([2, 2], [2, 3], 'k-', lw=2)
    ax.plot([2, 2], [7, 8], 'k-', lw=2)
    ax.text(2, 2.5, '+', fontsize=20, ha='center', va='center', color='red')
    ax.text(2, 7.5, '-', fontsize=20, ha='center', va='center', color='blue')
    ax.text(2, 5, 'Fonte\n5V', ha='center', va='center', fontweight='bold')
    
    # Resistência
    ax.add_patch(patches.Rectangle((5, 3.5), 2, 3, fill=True, color='lightcoral', ec='black', lw=2))
    ax.plot([4, 5], [5, 5], 'k-', lw=2)
    ax.plot([7, 8], [5, 5], 'k-', lw=2)
    ax.text(6, 5, 'R\n1kΩ', ha='center', va='center', fontweight='bold')
    
    # Capacitor
    ax.plot([8, 8], [3, 5], 'k-', lw=2)
    ax.plot([8, 8], [5, 7], 'k-', lw=2)
    ax.plot([7.7, 8.3], [3, 3], 'k-', lw=2)
    ax.plot([7.7, 8.3], [7, 7], 'k-', lw=2)
    ax.text(8.5, 5, 'C\n100μF', ha='left', va='center', fontweight='bold')
    
    # Fios de conexão
    ax.plot([2, 4], [2, 2], 'k-', lw=2)  # Fio inferior
    ax.plot([2, 4], [8, 8], 'k-', lw=2)  # Fio superior
    ax.plot([8, 9], [2, 2], 'k-', lw=2)  # Fio inferior direito
    ax.plot([8, 9], [8, 8], 'k-', lw=2)  # Fio superior direito
    ax.plot([9, 9], [2, 8], 'k-', lw=2)  # Fio vertical direito
    
    # Tensão no capacitor
    ax.text(6, 2.5, f'Vc = {V_c:.2f} V', ha='center', va='center', 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
            fontsize=12, fontweight='bold')
    
    # Corrente no circuito
    ax.annotate('', xy=(4.5, 2.5), xytext=(3.5, 2.5),
                arrowprops=dict(arrowstyle='->', lw=2, color='green'))
    ax.text(4, 2.2, f'I = {I*1000:.2f} mA', ha='center', va='top', 
            color='green', fontweight='bold')
    
    # Indicador de tempo
    tempo = tau * (V_c / V_fonte) * 5  # Estimativa do tempo decorrido
    ax.text(5, 9, f'τ = RC = {tau*1000:.1f} ms\nTempo: {tempo*1000:.1f} ms', 
            ha='center', va='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray'),
            fontsize=10)

# Configuração dos gráficos
def setup_plots():
    # Gráfico de tensão
    ax_tensao.clear()
    ax_tensao.grid(True, linestyle='--', alpha=0.7)
    ax_tensao.set_xlabel('Tempo (ms)')
    ax_tensao.set_ylabel('Tensão (V)')
    ax_tensao.set_title('Tensão no Capacitor vs. Tempo', fontweight='bold')
    ax_tensao.set_xlim(0, 5*tau*1000)
    ax_tensao.set_ylim(0, V_fonte * 1.1)
    
    # Gráfico de corrente
    ax_corrente.clear()
    ax_corrente.grid(True, linestyle='--', alpha=0.7)
    ax_corrente.set_xlabel('Tempo (ms)')
    ax_corrente.set_ylabel('Corrente (mA)')
    ax_corrente.set_title('Corrente no Circuito vs. Tempo', fontweight='bold')
    ax_corrente.set_xlim(0, 5*tau*1000)
    ax_corrente.set_ylim(0, (V_fonte/R) * 1000 * 1.1)
    
    # Adicionar linha vertical para constante de tempo
    ax_tensao.axvline(x=tau*1000, color='red', linestyle=':', alpha=0.7, label='τ = RC')
    ax_corrente.axvline(x=tau*1000, color='red', linestyle=':', alpha=0.7, label='τ = RC')
    
    ax_tensao.legend()
    ax_corrente.legend()

# Animação
def update(frame):
    # Para a animação, vamos usar apenas alguns pontos para melhor performance
    idx = frame * 10
    if idx >= len(t):
        idx = len(t) - 1
    
    V_c = V_capacitor[idx]
    I = I_circuito[idx]
    
    # Desenhar o circuito
    draw_circuit(ax_circuito, V_c, I)
    
    # Configurar os gráficos
    setup_plots()
    
    # Plotar dados até o frame atual
    ax_tensao.plot(t[:idx+1]*1000, V_capacitor[:idx+1], 'b-', linewidth=2, label='Vc(t)')
    ax_tensao.plot(t[idx]*1000, V_capacitor[idx], 'ro', markersize=8)
    
    ax_corrente.plot(t[:idx+1]*1000, I_circuito[:idx+1]*1000, 'g-', linewidth=2, label='I(t)')
    ax_corrente.plot(t[idx]*1000, I_circuito[idx]*1000, 'ro', markersize=8)
    
    # Adicionar anotações nos gráficos (SEM a caixa branca)
    ax_tensao.annotate(f'{V_capacitor[idx]:.2f} V', 
                       xy=(t[idx]*1000, V_capacitor[idx]),
                       xytext=(20, 20), textcoords='offset points',
                       arrowprops=dict(arrowstyle='->'))
    
    ax_corrente.annotate(f'{I_circuito[idx]*1000:.2f} mA', 
                         xy=(t[idx]*1000, I_circuito[idx]*1000),
                         xytext=(20, 20), textcoords='offset points',
                         arrowprops=dict(arrowstyle='->'))
    
    return ax_circuito, ax_tensao, ax_corrente

# Configuração inicial
draw_circuit(ax_circuito, 0, V_fonte/R)
setup_plots()

# Criar animação
ani = FuncAnimation(fig, update, frames=100, interval=50, blit=False)

plt.tight_layout()
plt.show()