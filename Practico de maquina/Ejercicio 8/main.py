import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import calcular_entropia_shannon as calcular_entropia

def calcular_capacidad_canal(matriz):
    """
    Realiza la búsqueda exhaustiva del espacio de entrada P(X) con paso 0.01
    para maximizar la Información Mutua I(X;Y).
    """
    max_I = -1.0
    mejor_px = None
    
    pasos = 100  # Genera incrementos de 0.01 (0.00, 0.01, ..., 1.00)

    for i in range(pasos + 1):
        p_x0 = i / 100.0
        p_x1 = 1.0 - p_x0
        P_X = [p_x0, p_x1]

        # a) Probabilidades de los símbolos de salida P(Y_j)
        # Teorema de la Probabilidad Total: P(y_j) = sum_i P(x_i) * P(y_j | x_i)
        P_Y = [0.0] * 4
        for j in range(4):
            P_Y[j] = P_X[0] * matriz[0][j] + P_X[1] * matriz[1][j]

        # b) Entropía de la salida H(Y) = - sum P(y_j) * log2(P(y_j))
        H_Y = calcular_entropia(P_Y)

        # c) Entropía condicional H(Y|X) (Ruido del canal):
        # H(Y|X) = sum_i P(x_i) * H(Y|X=x_i)
        H_Y_dado_X = 0.0
        for i_x in range(2):
            if P_X[i_x] > 0:
                h_fila = calcular_entropia(matriz[i_x])
                H_Y_dado_X += P_X[i_x] * h_fila

        # d) Información Mutua: I(X;Y) = H(Y) - H(Y|X)
        I_XY = H_Y - H_Y_dado_X

        # Maximización
        if I_XY > max_I:
            max_I = I_XY
            mejor_px = (p_x0, p_x1)

    return max_I, mejor_px

def ingresar_matriz():
    print("=== INGRESO DE LA MATRIZ DE TRANSICIÓN P(Y|X) (2x4) ===")
    print("Ingrese las probabilidades condicionales P(Y=y_j | X=x_i).")
    matriz = []
    #for i in range(2):
    i = 0
    while i < 2:
        j=0
        suma = 0.0
        fila=[]
        while j<4:
            valor = input(f"Ingresar P(Y={j} | X={i}) ")
            try:
                valor = float(valor)
            except ValueError:
                print("Error: Entrada inválida. Ingrese un número decimal.")
                continue
            if valor < 0 or valor > 1:
                print("Error: Las probabilidades deben estar entre 0 y 1.")
                continue
            suma += valor
            fila.append(valor)
            j += 1
        if suma != 1.0:
            print(f"Error: La suma de la fila {i} debe ser 1.0 (Suma actual: {suma:.5f}).")
            continue
        else:
          matriz.append(fila)
          i += 1  
    return matriz


   

if __name__ == "__main__":
    matriz = ingresar_matriz()

    capacidad, mejor_px = calcular_capacidad_canal(matriz)

    print("\n" + "="*55)
    print("RESULTADOS DE LA BÚSQUEDA EXHAUSTIVA DE CAPACIDAD DE CANAL")
    print("="*55)
    print(f"Capacidad del Canal (C): {capacidad:.6f} bits/símbolo")
    print(f"Distribución de entrada optimizada:")
    print(f"  P(X=0) = {mejor_px[0]:.2f}")
    print(f"  P(X=1) = {mejor_px[1]:.2f}")
    print("="*55)
