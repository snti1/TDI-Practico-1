# Cálculo de Capacidad de Canal por Búsqueda Exhaustiva (Binario a Cuaternario)

## 1. Descripción del Problema y Enunciado

El objetivo del ejercicio es desarrollar una aplicación en Python que determine la **Capacidad de Canal (C)** de un **sistema discreto sin memoria** con entrada binaria (q = 2 símbolos de entrada: X {0, 1}) y salida cuaternaria (s = 4 símbolos de salida: Y {0, 1, 2, 3}). 

El algoritmo implementado debe ser capaz de resolver la capacidad tanto para **canales uniformes** como **no uniformes** mediante un enfoque de optimización por **búsqueda exhaustiva (fuerza bruta)**.

### Requerimientos del Enunciado:
1. **Ingreso de la Matriz del Canal (P(Y|X)):**
   * Solicitar al usuario la carga por teclado de los 8 valores condicionales hacia adelante P(y_j|x_i) ordenados en una matriz de 2x4.
   * Validar numéricamente que las probabilidades pertenezcan al intervalo [0, 1] y que la suma de cada fila sea estrictamente igual a 1.0.
2. **Búsqueda Exhaustiva:**
   * Iterar el espacio de probabilidades de la fuente de entrada P(X) mediante incrementos de p = 0.01 en el rango [0.00, 1.00].
3. **Cálculo de Información Mutua I(X;Y):** En cada iteración calcular:
   * Probabilidades de los símbolos de salida P(Y_j) usando el **Teorema de la Probabilidad Total**.
   * Entropía de la salida H(Y).
   * Entropía condicional H(Y|X) (Ruido del canal).
   * Información Mutua I(X;Y) = H(Y) - H(Y|X).
4. **Maximización y Presentación:**
   * Almacenar el valor máximo de I(X;Y) alcanzado y la distribución de entrada óptima P(X=0), P(X=1).
   * Mostrar los resultados finales por pantalla expresados en bits/símbolo.

---

## 2. Fundamentos Matemáticos y Teoremas Aplicados

La resolución se apoya estrictamente en los principios formulados por Claude Shannon y la Teoría de la Información:

### A. Matriz de Transición de Probabilidades P(Y|X)
El canal discreto sin memoria se caracteriza estadísticamente por una matriz P(Y|X) de dimensión 2x4, donde cada elemento P(y_j|x_i) representa la probabilidad de recibir el símbolo y_j dado que se envió x_i. Cumple la propiedad estocástica: la suma de las probabilidades de cada fila da 1

### B. Teorema de la Probabilidad Total (Probabilidades de Salida P(Y))
Dada una distribución de entrada P(X) = [P(x_0), P(x_1)], la probabilidad marginal de cada símbolo de salida y_j se calcula como:
P(y_j) = sum_i P(x_i) * P(y_j | x_i)

### C. Entropía de Shannon H(Y)
La entropía mide la incertidumbre promedio o promedio de información proporcionado por la fuente de salida Y (expresada en bits/símbolo al usar logaritmo en base 2):
H(Y) = - sum P(y_j) * log2(P(y_j))

### D. Entropía Condicional / Ruido del Canal H(Y|X)
Representa la cantidad promedio de información inútil introducida aleatoriamente por el ruido del canal:
H(Y|X) = sum_i P(x_i) * H(Y|X=x_i)

### E. Información Mutua Promedio I(X;Y)
Es la cantidad real de información que la observación de las salidas Y proporciona sobre las entradas X. Mide la reducción de incertidumbre:
I(X;Y) = H(Y) - H(Y|X)

### F. Capacidad de Canal (C)
Se define como la máxima tasa de transmisión confiable de información posible a través del canal, maximizada sobre todas las distribuciones de probabilidad de entrada P(X):
C = max_{P(X)} I(X;Y)

---

## 3. Explicación Detallada de las Funciones del Código

A continuación se detalla el funcionamiento interno de cada función implementada en `capacidad_canal.py`:


### 1. `ingresar_matriz()`
* **Propósito:** Gestiona la lectura interactiva y validación estricta de la matriz de transición P(Y|X) de dimensión 2 x 4.
* **Mecanismo:**
  * Utiliza bucles `while` anidados para iterar sobre las 2 filas (i = 0, 1) y las 4 columnas (j = 0, 1, 2, 3).
  * Solicita cada valor individual P(Y=j | X=i) por teclado.
  * Captura excepciones `ValueError` si el usuario ingresa caracteres no numéricos.
  * Verifica que cada valor cumpla 0 <= valor <= 1.
  * Acumula la suma de la fila y verifica que sum_j P(Y=j|X=i) == 1.0. Si la suma difiere de 1.0, notifica el error y exige reingresar la fila completa.
  * Retorna la matriz validada como una lista de listas de Python `[[p00, p01, p02, p03], [p10, p11, p12, p13]]`.

### 2. `calcular_capacidad_canal(matriz)`
* **Propósito:** Ejecuta el algoritmo de **búsqueda exhaustiva** para encontrar la distribución de entrada P(X) que maximiza I(X;Y).
* **Mecanismo:**
  * Define `pasos = 100` para generar incrementos discretos de p = 0.01.
  * Barre el bucle `i` desde 0 hasta 100:
    * Define P(X=0) = i/100.0 y P(X=1) = 1.0 - P(X=0).
    * **Paso a:** Calcula P(Y) aplicando el Teorema de la Probabilidad Total multiplicando los pesos de P(X) por cada columna de la matriz de probabilidades condicionales.
    * **Paso b:** Calcula H(Y) invocando a `calcular_entropia(P_Y)` (de utils.py).
    * **Paso c:** Calcula la entropía condicional H(Y|X) ponderando la entropía de cada fila de la matriz condicional por su correspondiente P(X=i).
    * **Paso d:** Calcula la Información Mutua I(X;Y) = H(Y) - H(Y|X).
    * **Maximización:** Si I(X;Y) > max_I, actualiza la variable `max_I` con el nuevo valor récord y guarda la tupla de probabilidades óptimas `mejor_px = (p_x0, p_x1)`.
  * Retorna `(max_I, mejor_px)`.

### 3. Bloque Principal (`if __name__ == "__main__":`)
* Dirige el flujo de ejecución llamando a `ingresar_matriz()`, luego pasa la matriz a `calcular_capacidad_canal()`, e imprime en consola la Capacidad del Canal (C) formateada a 6 decimales y las probabilidades óptimas de entrada P(X=0) y P(X=1) formateadas a 2 decimales.

---
