import streamlit as st
import sympy as sp

# Definindo a fórmula de Manning
def manning_formula(n, A, R, S):
    return (1 / n) * A * R**(2/3) * S**(1/2)

# Calculando a altura e a velocidade de escoamento para diferentes formas
def calculate_height_velocity(shape, Q, b=1, n=0.013, S=0.0004, lambda_=1):
    y = sp.symbols('y')
    
    if shape == 'parabolic':
        A = b * y**2
        P = b + 2 * y
        R = A / P
    
    elif shape == 'triangular':
        A = (b * y) / 2
        P = b + 2 * y
        R = A / P
    
    elif shape == 'trapezoidal':
        A = b * y + lambda_ * y**2
        P = b + 2 * y * sp.sqrt(1 + lambda_**2)
        R = A / P
    
    elif shape == 'rectangular':
        A = b * y
        P = b + 2 * y
        R = A / P
    
    else:
        raise ValueError("Shape not recognized. Please use 'parabolic', 'triangular', 'trapezoidal', or 'rectangular'.")
    
    # Equação de Manning
    manning_eq = manning_formula(n, A, R, S) - Q
    
    # Solução da equação para y
    y_sol = sp.nsolve(manning_eq, y, 1)
    y_sol = float(y_sol)
    
    # Calculando a velocidade de escoamento
    A_sol = A.subs(y, y_sol)
    v = Q / A_sol
    
    return y_sol, v

# Título do app
st.title("Calculadora de Altura e Velocidade de Escoamento")

# Entradas do usuário
Q = st.number_input("Vazão (m³/s)", value=1.0, min_value=0.0, step=0.1)
b = st.number_input("Base do canal (m)", value=0.5, min_value=0.0, step=0.1)
n = st.number_input("Coeficiente de rugosidade de Manning", value=0.035, min_value=0.0, step=0.001)
S = st.number_input("Inclinação longitudinal (m/m)", value=0.005, min_value=0.0, step=0.001)
shape = st.selectbox("Forma do canal", ['parabolic', 'triangular', 'trapezoidal', 'rectangular'])

# Controle extra para lambda se a forma for trapezoidal
lambda_ = 1
if shape == 'trapezoidal':
    lambda_ = st.number_input("Inclinação lateral (λ)", value=2.0, min_value=0.0, step=0.1)

# Botão para calcular
if st.button("Calcular"):
    y, v = calculate_height_velocity(shape, Q, b, n, S, lambda_)
    
    st.write(f"Forma: {shape.capitalize()}")
    st.write(f"Altura da lâmina d'água (y): {y:.4f} m")
    st.write(f"Velocidade de escoamento (v): {v:.4f} m/s")
