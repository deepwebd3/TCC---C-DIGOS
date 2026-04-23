# Código Corrigido

def metodo_newton(x0, tol=1e-6, max_iter=10):
    """
    Implementação do método de Newton para encontrar raízes de f(x)

    Parâmetros:
    x0: aproximação inicial
    tol: tolerância (critério de parada)
    max_iter: número máximo de iterações

    Retorna:
    Aproximação da raiz ou None se não convergir
    """

    # Definindo a função e sua derivada (por diferenças centrais)
    def f(x):
        sigma = 5.67*10**(-8)
        h1 = 20
        T_inf = 300
        q = 100

        return sigma*x**4-h1*(x-T_inf)-q

    def df(x):
        h = 0.01
        return (f(x + h) - f(x - h)) / (2 * h)

    print("Iteração |     x     |   f(x)   |   Erro")
    print("------------------------------------------")

    for i in range(max_iter):
        fx = f(x0)
        dfx = df(x0)

        if abs(dfx) < 1e-12:
            print("\nDerivada muito próxima de zero. Método falhou.")
            return None

        x1 = x0 - fx / dfx
        erro = abs(x1 - x0)

        print(f"{i:8} | {x0:9.5f} | {fx:8.5f} | {erro:8.5f}")

        if erro < tol:
            print("\nConvergência alcançada!")
            return x1

        x0 = x1

    print("\nMétodo não convergiu após", max_iter, "iterações.")
    return None

# Chamadas de teste
print("=== Buscando a raiz positiva (x ≈ 2) ===")
raiz_positiva = metodo_newton(x0=310)
if raiz_positiva is not None:
    print(f"\nRaiz positiva encontrada: {raiz_positiva:.6f}")

# print("\n=== Buscando a raiz negativa (x ≈ -3) ===")
# raiz_negativa = metodo_newton(x0=-3.5)
# if raiz_negativa is not None:
#     print(f"\nRaiz negativa encontrada: {raiz_negativa:.6f}")
