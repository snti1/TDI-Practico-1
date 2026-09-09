import argparse

## INCISO A: DISTANCIA DE HAMMING
def distancia_hamming(str1, str2):
    
    if len(str1) != len(str2):
        raise ValueError(
            f"Error en Hamming. Las cadenas deben tener la misma longitud. "
            f"('{str1}' len={len(str1)} vs '{str2}' len={len(str2)})"
        )
    
    distancia = 0
    for char1, char2 in zip(str1, str2):
        if char1 != char2:
            distancia += 1
            
    return distancia


## INCISO B: DISTANCIA DE LEVENSHTEIN
def distancia_levenshtein(str1, str2):
    
    len1, len2 = len(str1), len(str2)
    
    # Matriz de (len1 + 1) x (len2 + 1)
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    # Casos base: transformar cadena vacía a la otra
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    # Llenado de la matriz por programación dinámica
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if str1[i - 1] == str2[j - 1]:
                costo_sustitucion = 0
            else:
                costo_sustitucion = 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,                  # Eliminación
                dp[i][j - 1] + 1,                  # Inserción
                dp[i - 1][j - 1] + costo_sustitucion # Sustitución
            )

    return dp[len1][len2]


## INCISO D: HEURÍSTICA Y NORMALIZACIÓN DE SIMILITUD
def calcular_similitud_normalizada(str1, str2):
    
    # Normalización
    s1_norm = str1.strip().lower()
    s2_norm = str2.strip().lower()

    dist = distancia_levenshtein(s1_norm, s2_norm)
    max_len = max(len(s1_norm), len(s2_norm))

    if max_len == 0:
        return 100.0, dist

    # Porcentaje de similitud relativa
    similitud = (1 - (dist / max_len)) * 100
    return similitud, dist


## PRUEBAS
def ejecutar_demostracion():
    print("============== DEMOSTRACIÓN INCISO A: Limitación de Hamming ==============")
    c1, c2 = "Juan Perez", "Jaun Perez"
    print(f"Comparando '{c1}' vs '{c2}':")
    try:
        d_h = distancia_hamming(c1, c2)
        print(f"  Distancia de Hamming: {d_h}")
        print("  > Nota: Aunque solo hay una transposición ('ua' -> 'au'), Hamming cuenta 2 sustituciones independientes porque no detecta desfases.")
    except ValueError as e:
        print(f"  Error: {e}")

    # Ejemplo con distinta longitud
    c3, c4 = "Juan Perez", "Juan  Perez"
    print(f"\nComparando '{c3}' vs '{c4}':")
    try:
        distancia_hamming(c3, c4)
    except ValueError as e:
        print(f"  > Falla esperada: {e}")

    print("\n============== INCISO C & D: Levenshtein y Heurística de Similitud ==============")
    casos_prueba = [
        ("Horacio López", "Oracio López"),
        ("Juan Perez", "Jaun Perez"),
        ("Teoría de la Información", "Teoria de la Informacion"),
        ("Algoritmo", "Algoritmos")
    ]

    for original, modificado in casos_prueba:
        d_lev = distancia_levenshtein(original, modificado)
        sim, _ = calcular_similitud_normalizada(original, modificado)
        print(f"• Cadena Original: '{original}' | Cadena Modificada: '{modificado}'")
        print(f"  - Distancia Levenshtein (errores): {d_lev}")
        print(f"  - Similitud relativa (normalizada): {sim:.2f}%\n")


## PARSER DE ARGUMENTOS
def parsear_argumentos():
    parser = argparse.ArgumentParser(
        description="Medición de Distancia y Similitud entre Cadenas de Texto."
    )
    parser.add_argument(
        "-s1", "--string1",
        type=str,
        help="Primera cadena a comparar."
    )
    parser.add_argument(
        "-s2", "--string2",
        type=str,
        help="Segunda cadena a comparar."
    )
    return parser.parse_args()


def main():
    args = parsear_argumentos()

    if args.string1 and args.string2:
        s1, s2 = args.string1, args.string2
        print(f"Comparando: '{s1}' vs '{s2}'\n")

        # Intentar Hamming si tienen igual largo
        if len(s1) == len(s2):
            print(f"Distancia de Hamming: {distancia_hamming(s1, s2)}")
        else:
            print("Distancia de Hamming: N/A (Distinta longitud)")

        d_lev = distancia_levenshtein(s1, s2)
        sim, _ = calcular_similitud_normalizada(s1, s2)
        print(f"Distancia de Levenshtein: {d_lev}")
        print(f"Porcentaje de Similitud: {sim:.2f}%")
    else:
        ejecutar_demostracion()


if __name__ == "__main__":
    main()