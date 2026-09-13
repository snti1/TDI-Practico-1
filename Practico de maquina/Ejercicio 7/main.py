def calcular_digito_verificador(cuil):
    # Pesos utilizados por el algoritmo de Módulo 11
    pesos = [5,4,3,2,7,6,5,4,3,2]
    suma = 0
    # Multiplicamos cada uno de los primeros 10 dígitos
    # por su peso correspondiente
    for i in range(10):
        suma += int(cuil[i]) * pesos[i]
    resto = suma % 11
    digito = 11-resto
    # Casos especiales del algoritmo
    if digito == 11:
        digito = 0
    elif digito == 10:
        digito = 9
    return digito


# Pedimos el cuil/CUIL
if __name__ == "__main__":
    cuil = input("Ingrese un CUIT/CUIL de 11 dígitos: ")

    # Validamos que tenga exactamente 11 dígitos
    if len(cuil) != 11 or not cuil.isdigit():
        print("Entrada inválida: debe ingresar su cuit/cuil de la siguiente manera: 20123456781")
    else:
        # Calculamos el dígito esperado usando los primeros 10
        digito_esperado = calcular_digito_verificador(cuil)
        # Obtenemos el dígito ingresado
        digito_ingresado = int(cuil[10])
        # Comparamos ambos
        if digito_esperado == digito_ingresado:
            print("Su codigo de verificación es Válido")
        else:
            print("Su codigo de verificación es Inválido")