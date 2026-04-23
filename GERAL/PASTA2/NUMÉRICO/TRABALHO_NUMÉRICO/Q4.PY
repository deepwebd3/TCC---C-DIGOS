import numpy as np

def von_karman(f, Re):
    """Função que representa a equação de von Karman reorganizada para cálculo do fator de atrito."""
    if f <= 0:
        return np.inf  # Evita erro por raiz negativa
    return 1/np.sqrt(f) - 4 * np.log10(Re * np.sqrt(f)) + 0.4

def calcular_fator_atrito(Re, a=0.001, b=0.01, tol=5e-6, max_iter=1000):
    """
    Calcula o fator de atrito de Fanning usando o método da bissecção.
    
    Parâmetros:
        Re - Número de Reynolds
        a - Limite inferior inicial do intervalo
        b - Limite superior inicial do intervalo
        tol - Tolerância (erro absoluto desejado)
        max_iter - Número máximo de iterações
    
    Retorna:
        O fator de atrito de Fanning calculado
    """
    # Verificação inicial do intervalo
    fa = von_karman(a, Re)
    fb = von_karman(b, Re)
    
    if fa * fb > 0:
        raise ValueError("A função não muda de sinal no intervalo fornecido. Tente ajustar os limites a e b.")

    # Método da bissecção
    for i in range(max_iter):
        c = (a + b) / 2
        fc = von_karman(c, Re)

        # Critérios de parada
        if abs(fc) < tol or (b - a)/2 < tol:
            return c
        
        # Atualização do intervalo
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    raise RuntimeError(f"Não convergiu após {max_iter} iterações")

def interface_usuario():
    """Função para interação com o usuário e cálculo do fator de atrito."""
    print("Calculadora do Fator de Atrito de Fanning")
    print("----------------------------------------")
    print("Esta calculadora resolve a equação de von Karman para escoamento turbulento")
    print("em tubos rugosos, usando o método da bissecção com precisão de 0.000005.\n")
    
    while True:
        try:
            # Obter número de Reynolds do usuário
            Re = float(input("Digite o número de Reynolds (Re > 2300): "))
            
            if Re <= 2300:
                print("Para Re ≤ 2300 (regime laminar), use f = 16/Re")
                continue
                
            # Calcular fator de atrito
            f = calcular_fator_atrito(Re)
            
            # Mostrar resultados
            print(f"\nResultados para Re = {Re:.2f}:")
            print(f"Fator de Fanning (f): {f:.7f}")
            print(f"Fator de Darcy (fD): {4*f:.7f} (4 × fator de Fanning)")
            print(f"Erro absoluto garantido: < 0.000005\n")
            
            # Opção para novo cálculo
            continuar = input("Deseja calcular para outro Re? (s/n): ").strip().lower()
            if continuar != 's':
                break
                
        except ValueError as e:
            print(f"Erro: {e}. Por favor, insira um valor numérico válido.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

# Executar a interface do usuário
if __name__ == "__main__":
    interface_usuario()