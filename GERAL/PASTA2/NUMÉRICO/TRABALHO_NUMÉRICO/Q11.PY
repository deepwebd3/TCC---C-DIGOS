import numpy as np
import matplotlib.pyplot as plt

# Parâmetros físicos
g = 9.81  # aceleração da gravidade (m/s²)
c = 0.1   # coeficiente de arrasto (kg/m)
m = 1.0   # massa do projétil (kg)
v0 = 300  # velocidade inicial (m/s)
theta = np.deg2rad(45)  # ângulo de lançamento (convertido para radianos)

# Condições iniciais
x0 = 0.0
y0 = 0.0
vx0 = v0 * np.cos(theta)
vy0 = v0 * np.sin(theta)

# Função que define o sistema de EDOs
def derivadas(state, t):
    x, y, vx, vy = state
    v = np.sqrt(vx**2 + vy**2)
    
    dxdt = vx
    dydt = vy
    dvxdt = -(c/m) * v * vx
    dvydt = -g - (c/m) * v * vy
    
    return np.array([dxdt, dydt, dvxdt, dvydt])

# Parâmetros da simulação
h = 0.01  # passo de tempo (s)
t_max = 100.0  # tempo máximo de simulação (s)

# Inicialização
t_pontos = np.arange(0, t_max, h)
states = np.zeros((len(t_pontos), 4))  # matriz para armazenar x, y, vx, vy
states[0] = [x0, y0, vx0, vy0]

# Método de Runge-Kutta de 4ª ordem
for i in range(1, len(t_pontos)):
    state = states[i-1]
    t = t_pontos[i-1]
    
    k1 = h * derivadas(state, t)
    k2 = h * derivadas(state + 0.5*k1, t + 0.5*h)
    k3 = h * derivadas(state + 0.5*k2, t + 0.5*h)
    k4 = h * derivadas(state + k3, t + h)
    
    states[i] = state + (k1 + 2*k2 + 2*k3 + k4)/6
    
    # Parar a simulação quando o projétil atingir o solo (y <= 0)
    if states[i,1] <= 0:
        # Interpolação linear para encontrar o ponto exato de impacto
        y_prev = states[i-1,1]
        y_curr = states[i,1]
        alpha = y_prev / (y_prev - y_curr)
        
        # Ajustar o último estado para y = 0
        states[i] = states[i-1] + alpha*(states[i] - states[i-1])
        t_pontos = t_pontos[:i+1]
        states = states[:i+1]
        break

# Extrair resultados
x = states[:,0]
y = states[:,1]
vx = states[:,2]
vy = states[:,3]

# Calcular quantidades de interesse
alcance = x[-1]  # último valor de x quando y = 0
tempo_voo = t_pontos[-1]  # último tempo da simulação
altura_max = np.max(y)  # valor máximo de y

# Resultados
print(f"Alcance horizontal máximo: {alcance:.2f} m")
print(f"Tempo total de voo: {tempo_voo:.2f} s")
print(f"Altura máxima atingida: {altura_max:.2f} m")

# Plotar trajetória
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2)
plt.plot(x[-1], y[-1], 'ro', label=f'Ponto de impacto: {alcance:.1f}m')
plt.title('Trajetória do Projétil com Arrasto Quadrático')
plt.xlabel('Distância horizontal (m)')
plt.ylabel('Altura (m)')
plt.grid(True)
plt.legend()
plt.axis('equal')
plt.show()