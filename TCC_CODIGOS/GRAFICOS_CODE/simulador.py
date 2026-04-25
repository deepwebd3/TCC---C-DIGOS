import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
from matplotlib.widgets import Button

# ======================
# CONFIGURAÇÃO VISUAL
# ======================
plt.rcParams.update({
    'font.family': 'Times New Roman',
    'font.size': 12,
    'axes.linewidth': 1.5,
    'axes.titleweight': 'bold',
    'axes.titlesize': 14
})

# ======================
# PARÂMETROS DO CIRCUITO RC
# ======================
R = 1000      # Ohms
C = 100e-6    # Farads (100 µF)
V_fonte = 5   # Volts
tau = R * C   # Constante de tempo RC

t = np.linspace(0, 5*tau, 1000)
V_capacitor = V_fonte * (1 - np.exp(-t/tau))
I_circuito = (V_fonte/R) * np.exp(-t/tau)

# ======================
# FIGURA E LAYOUT
# ======================
fig = plt.figure(figsize=(15, 9))
fig.suptitle('Simulação de Circuito RC - Resposta Transitória',
             fontsize=16, fontweight='bold', y=0.96)

grid = plt.GridSpec(3, 2, width_ratios=[1, 1], height_ratios=[1, 1, 1],
                    wspace=0.35, hspace=0.55, top=0.9, bottom=0.15)

ax_circuito = fig.add_subplot(grid[0, 0])
ax_tensao = fig.add_subplot(grid[1, :])
ax_corrente = fig.add_subplot(grid[2, :])

# ======================
# BOTÕES DE CONTROLE
# ======================
ax_play = plt.axes([0.18, 0.02, 0.1, 0.05])
ax_pause = plt.axes([0.32, 0.02, 0.1, 0.05])
ax_reset = plt.axes([0.46, 0.02, 0.1, 0.05])

btn_play = Button(ax_play, '▶ Iniciar', color='lightgreen', hovercolor='limegreen')
btn_pause = Button(ax_pause, '⏸ Pausar', color='lightcoral', hovercolor='red')
btn_reset = Button(ax_reset, '🔄 Reiniciar', color='lightblue', hovercolor='dodgerblue')

anim_running = True

def play(event):
    global anim_running
    anim_running = True
    ani.event_source.start()

def pause(event):
    global anim_running
    anim_running = False
    ani.event_source.stop()

def reset(event):
    global anim_running
    anim_running = True
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.stop()
    ani.event_source.start()

btn_play.on_clicked(play)
btn_pause.on_clicked(pause)
btn_reset.on_clicked(reset)

# ======================
# FUNÇÃO PARA DESENHAR O CIRCUITO
# ======================
def draw_circuit(ax, Vc, I):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_aspect('equal')
    ax.set_title('Circuito RC - Modelo Visual', pad=20, fontsize=14, fontweight='bold')

    # Fios
    ax.plot([1, 9], [6, 6], 'k-', lw=2)   # linha superior
    ax.plot([1, 9], [2, 2], 'k-', lw=2)   # linha inferior
    ax.plot([9, 9], [2, 6], 'k-', lw=2)   # retorno direito

    # Fonte
    ax.add_patch(patches.Circle((1, 4), 0.7, color='lightblue', ec='black', lw=2))
    ax.text(1, 4, "5V", ha='center', va='center', fontweight='bold')
    ax.text(1, 6.4, "+", fontsize=18, color='red', ha='center')
    ax.text(1, 1.6, "−", fontsize=18, color='blue', ha='center')

    # Resistência (centralizada)
    ax.add_patch(patches.Rectangle((3.5, 5.25), 2, 1.5, facecolor='salmon', edgecolor='black', lw=2))
    ax.text(4.5, 6, "R = 1kΩ", ha='center', va='center', fontweight='bold')

    # Capacitor (com espaçamento e legenda ajustados)
    ax.plot([7.5, 7.5], [2.7, 5.3], 'k-', lw=2)
    ax.plot([8, 8], [2.7, 5.3], 'k-', lw=2)
    ax.text(8.3, 4, "C = 100μF", ha='left', va='center', fontweight='bold')

    # Corrente (seta verde)
    ax.annotate('', xy=(3.3, 1.8), xytext=(2.2, 1.8),
                arrowprops=dict(arrowstyle='->', lw=2, color='green'))
    ax.text(2.8, 1.2, f"I = {I*1000:.2f} mA", color='green', ha='center', fontweight='bold')

    # Tensão no capacitor (sem fundo branco)
    ax.text(5.5, 1, f"Vc = {Vc:.2f} V", ha='center', va='center',
            color='darkorange', fontweight='bold')

    # Tempo e constante RC
    ax.text(5, 7.4, f"τ = {tau*1000:.1f} ms",
            ha='center', fontsize=10, fontstyle='italic', alpha=0.8)

# ======================
# CONFIGURAÇÃO DOS GRÁFICOS
# ======================
def setup_plots():
    ax_tensao.clear()
    ax_corrente.clear()

    # --- Gráfico de Tensão ---
    ax_tensao.grid(True, linestyle='--', alpha=0.7)
    ax_tensao.set_xlim(0, 5*tau*1000)
    ax_tensao.set_ylim(0, V_fonte * 1.1)
    ax_tensao.set_title('Tensão no Capacitor', pad=15, fontweight='bold')
    ax_tensao.set_xlabel('Tempo (ms)', fontweight='bold')
    ax_tensao.set_ylabel('Tensão (V)', fontweight='bold')
    ax_tensao.axvline(x=tau*1000, color='red', linestyle=':', alpha=0.7, label='τ = RC')
    ax_tensao.legend(loc='lower right', framealpha=0.9)

    # --- Gráfico de Corrente ---
    ax_corrente.grid(True, linestyle='--', alpha=0.7)
    ax_corrente.set_xlim(0, 5*tau*1000)
    ax_corrente.set_ylim(0, (V_fonte/R) * 1000 * 1.1)
    ax_corrente.set_title('Corrente no Circuito', pad=15, fontweight='bold')
    ax_corrente.set_xlabel('Tempo (ms)', fontweight='bold')
    ax_corrente.set_ylabel('Corrente (mA)', fontweight='bold')
    ax_corrente.axvline(x=tau*1000, color='red', linestyle=':', alpha=0.7, label='τ = RC')
    ax_corrente.legend(loc='upper right', framealpha=0.9)

# ======================
# FUNÇÃO DE ATUALIZAÇÃO
# ======================
def update(frame):
    idx = frame * 10
    if idx >= len(t):
        idx = len(t) - 1
    Vc = V_capacitor[idx]
    I = I_circuito[idx]

    draw_circuit(ax_circuito, Vc, I)
    setup_plots()

    # Trajetórias
    ax_tensao.plot(t[:idx+1]*1000, V_capacitor[:idx+1], 'b-', lw=2)
    ax_corrente.plot(t[:idx+1]*1000, I_circuito[:idx+1]*1000, 'g-', lw=2)

    # Pontos marcados
    ax_tensao.plot(t[idx]*1000, V_capacitor[idx], 'ro', markersize=8)
    ax_corrente.plot(t[idx]*1000, I_circuito[idx]*1000, 'ro', markersize=8)

    # Anotações (sem caixas brancas)
    ax_tensao.annotate(f'{V_capacitor[idx]:.2f} V',
                       xy=(t[idx]*1000, V_capacitor[idx]),
                       xytext=(15, 20), textcoords='offset points',
                       arrowprops=dict(arrowstyle='->', color='red'),
                       color='black', fontweight='bold')

    ax_corrente.annotate(f'{I_circuito[idx]*1000:.2f} mA',
                         xy=(t[idx]*1000, I_circuito[idx]*1000),
                         xytext=(15, 20), textcoords='offset points',
                         arrowprops=dict(arrowstyle='->', color='red'),
                         color='black', fontweight='bold')

    return ax_circuito, ax_tensao, ax_corrente

# ======================
# EXECUÇÃO
# ======================
draw_circuit(ax_circuito, 0, V_fonte/R)
setup_plots()

ani = FuncAnimation(fig, update, frames=100, interval=50, blit=False, repeat=False)

fig.text(0.02, 0.025, 'Simulação de Circuito RC - Engenharia Elétrica',
         fontsize=10, style='italic', alpha=0.7)

plt.tight_layout(rect=[0, 0.08, 1, 0.95])
plt.show()