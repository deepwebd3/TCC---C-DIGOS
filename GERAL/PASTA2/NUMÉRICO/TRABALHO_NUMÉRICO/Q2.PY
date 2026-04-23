import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Dados dos pontos
x = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
y = np.array([0.95, 1.48, 2.10, 2.52, 2.97, 3.52, 4.21, 4.55, 5.02, 5.51, 6.19, 6.88, 7.32, 8.05])

# Número de pontos
n = len(x)

# Cálculos necessários para ajuste linear manual
sum_x = np.sum(x)
sum_y = np.sum(y)
sum_xy = np.sum(x * y)
sum_x2 = np.sum(x ** 2)

# Coeficientes da reta y = ax + b
a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
b = (sum_y - a * sum_x) / n
print(f"Equação da reta ajustada: y = {a:.4f}x + {b:.4f}")

# Valores ajustados pelo modelo linear
y_ajustada = a * x + b

# Plot do ajuste linear
plt.scatter(x, y, label='Pontos originais', color='blue')
plt.plot(x, y_ajustada, label='Reta ajustada', color='red')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Ajuste de reta pelo Método dos Mínimos Quadrados')
plt.legend()
plt.grid(True)
plt.show()

# Métricas do modelo linear
R_squared = 1 - (np.sum((y - y_ajustada) ** 2) / np.sum((y - np.mean(y)) ** 2))
MSE = np.mean((y - y_ajustada) ** 2)
residuos = y - y_ajustada
print(f"Inclinação (a): {a:.4f}")
print(f"Coeficiente de determinação (R²): {R_squared:.4f}")
print(f"Erro quadrático médio (MSE): {MSE:.4f}")
print(f"Desvio padrão dos resíduos: {np.std(residuos):.4f}")

# Ajuste do modelo quadrático y = ax^2 + bx + c
coef_quadratico = np.polyfit(x, y, 2)
a2, b2, c2 = coef_quadratico
y_quadratica = a2 * x**2 + b2 * x + c2
print(f"Equação do modelo quadrático ajustado: y = {a2:.4f}x^2 + {b2:.4f}x + {c2:.4f}")

# Plot dos modelos linear e quadrático
plt.scatter(x, y, label='Pontos originais', color='blue')
plt.plot(x, y_ajustada, label='Reta ajustada (linear)', color='red')
plt.plot(x, y_quadratica, label='Curva ajustada (quadrática)', color='green')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Ajuste Linear e Quadrático pelo Método dos Mínimos Quadrados')
plt.legend()
plt.grid(True)
plt.show()

# Comparação de R² dos dois modelos
R_squared_linear = 1 - (np.sum((y - y_ajustada) ** 2) / np.sum((y - np.mean(y)) ** 2))
R_squared_quadratic = 1 - (np.sum((y - y_quadratica) ** 2) / np.sum((y - np.mean(y)) ** 2))
print(f"R² (linear): {R_squared_linear:.4f}")
print(f"R² (quadrático): {R_squared_quadratic:.4f}")

# ========================
# Validação cruzada com train-test split
# ========================
X = x.reshape(-1, 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo linear
modelo_linear = LinearRegression()
modelo_linear.fit(X_train, y_train)
y_pred_linear = modelo_linear.predict(X_test)

# Modelo quadrático
X_train_quad = np.column_stack((X_train**2, X_train))
X_test_quad = np.column_stack((X_test**2, X_test))
modelo_quadratico = LinearRegression()
modelo_quadratico.fit(X_train_quad, y_train)
y_pred_quadratico = modelo_quadratico.predict(X_test_quad)

# Métricas no conjunto de teste
mse_linear = mean_squared_error(y_test, y_pred_linear)
r2_linear = r2_score(y_test, y_pred_linear)

mse_quadratico = mean_squared_error(y_test, y_pred_quadratico)
r2_quadratico = r2_score(y_test, y_pred_quadratico)

print("\nValidação com train-test split:")
print(f"Linear -> MSE: {mse_linear:.4f}, R²: {r2_linear:.4f}")
print(f"Quadrático -> MSE: {mse_quadratico:.4f}, R²: {r2_quadratico:.4f}")