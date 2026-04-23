import numpy as np

# Dados fornecidos
E = 200000  # MPa
sigma_m = 250  # MPa
ec_k2 = 0.4
Lk = 50

# Função para resolver f(x) = 0
def func(x):
    theta = 0.5 * np.sqrt(x / E) * Lk
    if np.cos(theta) == 0:  # evita divisão por zero
        return np.inf
    sec_theta = 1 / np.cos(theta)
    return sigma_m / (1 + ec_k2 * sec_theta) - x

# Método da bisseção
def bissecao(f, a, b, tol=1e-4, max_iter=100):
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
    raise RuntimeError("Máximo de iterações excedido.")

# Intervalo de chute inicial (em MPa)
a = 1
b = 250

# Resolvendo
PA = bissecao(func, a, b)
print(f"O valor de P/A é aproximadamente {PA:.4f} MPa")
# Cálculo do fator de segurança
fator_segurança = sigma_m / PA
print(f"O fator de segurança é aproximadamente {fator_segurança:.4f}")
# Cálculo do deslocamento angular
theta = 0.5 * np.sqrt(PA / E) * Lk
print(f"O deslocamento angular é aproximadamente {theta:.4f} radianos")