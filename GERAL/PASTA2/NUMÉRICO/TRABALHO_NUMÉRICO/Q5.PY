import numpy as np

# Constantes fornecidas
u = 2000          # velocidade de exaustão (m/s)
m0 = 150000       # massa inicial (kg)
q = 2700          # taxa de consumo de combustível (kg/s)
g = 9.81          # aceleração da gravidade (m/s²)
v_desejada = 750  # velocidade desejada (m/s)

# Função baseada na equação do foguete
def func(t):
    if m0 - q * t <= 0:
        return np.inf  # evita log de número negativo ou zero
    return u * np.log(m0 / (m0 - q * t)) - g * t - v_desejada

# Método da bisseção
def bissecao(f, a, b, tol=1e-2, max_iter=100):
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError("A função não muda de sinal no intervalo.")

    for _ in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        if abs(fc) < tol or (b - a) / 2 < tol:
            return c

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    raise RuntimeError("Número máximo de iterações excedido.")

# Intervalo inicial sugerido no enunciado
t_inicial = 10
t_final = 50

# Encontrando o tempo t usando bisseção
t_resultado = bissecao(func, t_inicial, t_final)
print(f"O instante em que a velocidade é 750 m/s é aproximadamente t = {t_resultado:.4f} segundos.")