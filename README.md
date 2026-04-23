# ⚡ ESTUDO DOS METODOS DE RUNGE-KUTTA DE PRIMEIRA A QUARTA ORDEM APLICADOS A CIRCUITOS ELÉTRICOS RC

## 📌 Descrição

Este projeto investiga o fenômeno de eletrização de um automóvel em movimento causado pelo atrito com o solo, modelando o sistema como um circuito **elétrico do tipo Resistor-Capacitor (RC)**. Além disso, são analisados dois circuitos RC de forma independente: o EX2, que representa um processo de descarga, e o EX3, que descreve o carregamento do circuito.

Durante o movimento, o veículo acumula carga elétrica e, ao parar, essa carga é dissipada pelos pneus. Caso a descarga não ocorra completamente, pode surgir uma diferença de potencial capaz de gerar uma centelha e inflamar o combustível.

Os problemas são descritos por **Equações Diferenciais Ordinárias (EDOs)** de primeira ordem, cujas soluções são obtidas por meio de métodos **numéricos de Runge-Kutta (RK1 a RK4)**.

---

## 🎯 Objetivos

- Modelar a descarga elétrica do veículo como circuito RC  
- Aplicar métodos de Runge-Kutta (RK1 a RK4)  
- Comparar soluções numéricas com a solução analítica  
- Avaliar o erro relativo dos métodos  
- Determinar o tempo seguro para evitar ignição (U < 50 mJ)

---

## ⚙️ Modelo Matemático

A partir da modelagem matemática do circuito elétrico do tipo RC, tem-se a seguinte equação diferencial ordinária:

dt
dV
	​

=−
(25×10
9
)(500×10
−12
)
1
	​

V
(40)

Aplicando o método de separação de variáveis, obtém-se:

∫
V
dV
	​

=∫−
(25×10
9
)(500×10
−12
)
1
	​

dt
(41)

Após integrar ambos os lados:

ln(V)=−
12,5
t
	​

+K
(42)

Aplicando a exponencial:

V(t)=Ke
−t/12,5
(43)

Utilizando a condição inicial V(0)=30, temos:

30=Ke
0
⇒K=30

Logo, a solução final para a tensão é:

V(t)=30e
−t/12,5
(44)
⚡ Energia no Capacitor

De acordo com a literatura, a energia armazenada em um capacitor é dada por:

U=
2C
q
2
	​

(45)

Durante o processo de descarga, a carga elétrica varia conforme:

q(t)=q
0
	​

e
−t/RC
(46)

Sabendo que q
0
	​

=CV
0
	​

, substituindo na equação da energia:

U(t)=
2C
(CV
0
	​

e
−t/RC
)
2
	​

(47)

Simplificando:

U(t)=
2
CV
0
2
	​

	​

e
−2t/RC
(48)
⏱️ Determinação do Tempo Crítico

Para determinar o tempo em que a energia atinge o valor crítico U, isolamos a exponencial:

e
−2t/RC
=
(CV
0
	​

)
2
2U
	​

(49)

Substituindo os valores do problema:

e
−2t/[(25×10
9
)(500×10
−12
)]
=
[(500×10
−12
)(30×10
3
)]
2
2(50×10
−3
)
	​

(50)

Aplicando logaritmo natural:

−
(25×10
9
)(500×10
−12
)
2t
	​

=ln(
[(500×10
−12
)(30×10
3
)]
2
2(50×10
−3
)
	​

)
(51)

Isolando t:

t=−
2
(25×10
9
)(500×10
−12
)
	​

ln(
[(500×10
−12
)(30×10
3
)]
2
2(50×10
−3
)
	​

)
(52)
✅ Resultado Final

O tempo analítico obtido para o decaimento da energia crítica é:

t≈9,4005 s

## Equações

$$
\frac{dV}{dt} = -\frac{V}{R_{eq}C}
$$

$$
V(t) = V_0 e^{-t/(R_{eq}C)}
$$

$$
U(t) = \frac{1}{2} C V(t)^2
$$

---

## 🔬 Parâmetros de EX1 >>> carro-eletrizado

| Parâmetro | Valor |
|----------|------|
| Tensão inicial (V₀) | 30 kV |
| Capacitância (C) | 500 pF |
| Resistência dos pneus (R) | 100 GΩ |
| Resistência equivalente (R_eq) | R / 4 |
| Energia crítica (U_fogo) | 50 mJ |

---

## 🧪 Métodos Numéricos Utilizados

- Euler (RK1)  
- Heun (RK2)  
- Runge-Kutta de 3ª ordem (RK3)  
- Runge-Kutta de 4ª ordem (RK4)

---

## 📊 Gráficos

### 🔹 Comparação dos métodos de RK para o EX 1 - carro-eletrizado
![Tensão](TCC_CODIGOS/GRAFICOS_PNG/grafico1.png)

### 🔹 Comparação dos métodos de RK para o EX 2 - circuito RC descarregando
![Comparação RK](TCC_CODIGOS/GRAFICOS_PNG/grafico2.png)

### 🔹 Comparação dos métodos de RK para o EX 3 - circuito RC carregando
![Energia](TCC_CODIGOS/GRAFICOS_PNG/grafico3.png)

### 🔹 Relação de tensão e energia para o EX1 - carro-eletrizado
![Tensão e Energia](TCC_CODIGOS/GRAFICOS_PNG/tensao_energia.png)

---

## 🎞️ Simulação do Circuito RC

![Simulação RC](TCC_CODIGOS/GRAFICOS_PNG/simulacao_rc.gif)

---

## 🚀 Como executar

```bash
git clone https://github.com/deepwebd3/TCC---C-DIGOS.git
cd TCC---C-DIGOS

# Criar ambiente virtual
python -m venv .venv

# Ativar (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Executar simulação
python TCC_CODIGOS/EX3.py