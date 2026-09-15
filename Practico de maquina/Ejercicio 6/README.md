# Medición de distancia y similitud entre cadenas

**Teoría de la Información — Práctico de Máquina 1, Ejercicio 6**

## Descripción

Este programa compara dos cadenas de texto y determina su diferencia mediante dos métricas:

- Distancia de Hamming.
- Distancia de Levenshtein.

También calcula un porcentaje de similitud normalizada basado en la distancia de Levenshtein.

El objetivo es analizar cuánto se modificó un mensaje respecto del original y mostrar por qué la distancia de Hamming no es adecuada cuando las cadenas tienen distinta longitud o sufren desplazamientos.

El programa puede ejecutarse de dos maneras:

- Sin argumentos, para correr una demostración con casos predefinidos.
- Con dos cadenas ingresadas mediante argumentos, para realizar una comparación personalizada.

## Distancia de Hamming

La distancia de Hamming cuenta cuántas posiciones contienen caracteres diferentes:

$d_H(x,y) = \sum_{i=1}^{n} [x_i \neq y_i]$

Solo puede aplicarse cuando ambas cadenas tienen exactamente la misma longitud.

Por ejemplo:

```text
Juan Perez
Jaun Perez
```

Aunque el error visual es una transposición de `u` y `a`, Hamming compara las posiciones individualmente:

```text
Juan Perez
Jaun Perez
 ^^
```

Por lo tanto:

```text
Distancia de Hamming = 2
```

Si las cadenas poseen distinta longitud, la función genera un `ValueError`.

## Distancia de Levenshtein

La distancia de Levenshtein calcula la cantidad mínima de operaciones necesarias para transformar una cadena en la otra.

Las operaciones permitidas son:

- Inserción de un carácter.
- Eliminación de un carácter.
- Sustitución de un carácter.

La recurrencia utilizada es:

$D(i,j) = \min(D(i-1,j)+1,\ D(i,j-1)+1,\ D(i-1,j-1)+c)$

donde:

```text
c = 0, si los caracteres son iguales
c = 1, si los caracteres son diferentes
```

La implementación utiliza una matriz de programación dinámica de tamaño:

```text
(len(str1) + 1) × (len(str2) + 1)
```

Cada posición `dp[i][j]` contiene la distancia mínima entre los primeros `i` caracteres de la primera cadena y los primeros `j` caracteres de la segunda.

## Similitud normalizada

Antes de calcular la similitud, las cadenas se normalizan mediante:

```python
s1_norm = str1.strip().lower()
s2_norm = str2.strip().lower()
```

Esto:

- Elimina espacios al principio y al final.
- Convierte los caracteres a minúsculas.

Luego se calcula:

$Similitud = \left(1 - \frac{d_L(x,y)}{\max(|x|,|y|)}\right) \times 100$

donde `d_L` es la distancia de Levenshtein.

Si ambas cadenas están vacías, la función devuelve:

```text
Similitud = 100 %
Distancia = 0
```

## Ejecución

### Ejecutar la demostración

Si no se proporcionan argumentos, se ejecutan automáticamente los casos de prueba:

```bash
python main.py
```

Los casos incluidos son:

```text
"Juan Perez" vs. "Jaun Perez"
"Juan Perez" vs. "Juan  Perez"
"Horacio López" vs. "Oracio López"
"Teoría de la Información" vs. "Teoria de la Informacion"
"Algoritmo" vs. "Algoritmos"
```

### Comparar dos cadenas

```bash
python main.py -s1 "Horacio López" -s2 "Oracio López"
```

También pueden utilizarse las opciones completas:

```bash
python main.py --string1 "Juan Perez" --string2 "Jaun Perez"
```

Las comillas son necesarias cuando una cadena contiene espacios.

### Mostrar la ayuda

```bash
python main.py --help
```

```text
usage: main.py [-h] [-s1 STRING1] [-s2 STRING2]

Medición de Distancia y Similitud entre Cadenas de Texto.

options:
  -h, --help            show this help message and exit
  -s1 STRING1, --string1 STRING1
                        Primera cadena a comparar.
  -s2 STRING2, --string2 STRING2
                        Segunda cadena a comparar.
```

Para ejecutar una comparación personalizada deben proporcionarse los dos argumentos. Si falta uno, el código actual ejecuta la demostración completa.

## Ejemplo de salida

Comparación personalizada:

```text
Comparando: 'Horacio López' vs 'Oracio López'

Distancia de Hamming: N/A (Distinta longitud)
Distancia de Levenshtein: 1
Porcentaje de Similitud: 92.31%
```

Demostración de la limitación de Hamming:

```text
============== DEMOSTRACIÓN INCISO A: Limitación de Hamming ==============
Comparando 'Juan Perez' vs 'Jaun Perez':
  Distancia de Hamming: 2
  > Nota: Aunque solo hay una transposición ('ua' -> 'au'),
    Hamming cuenta 2 sustituciones independientes porque no detecta desfases.

Comparando 'Juan Perez' vs 'Juan  Perez':
  > Falla esperada: Error en Hamming. Las cadenas deben tener la misma longitud.
```

Demostración de Levenshtein y similitud:

```text
============== INCISO C & D: Levenshtein y Heurística de Similitud ==============
• Cadena Original: 'Horacio López' | Cadena Modificada: 'Oracio López'
  - Distancia Levenshtein (errores): 1
  - Similitud relativa (normalizada): 92.31%

• Cadena Original: 'Algoritmo' | Cadena Modificada: 'Algoritmos'
  - Distancia Levenshtein (errores): 1
  - Similitud relativa (normalizada): 90.00%
```

Los valores dependen de las cadenas ingresadas y de la normalización aplicada.

## Explicación teórica

La distancia de Hamming es adecuada cuando dos mensajes tienen la misma longitud y cada posición se corresponde directamente. Por ejemplo, permite contar bits alterados en dos tramas binarias del mismo tamaño.

Sin embargo, una inserción o eliminación desplaza los caracteres posteriores. Hamming interpreta ese desplazamiento como múltiples sustituciones o directamente no puede procesarlo si cambia la longitud.

Levenshtein resuelve esta limitación porque considera inserciones, eliminaciones y sustituciones. Por eso resulta más apropiada para nombres mal escritos, errores de tipeo y mensajes que pueden haber sufrido pérdidas o agregados.

La similitud normalizada transforma la distancia absoluta en un porcentaje relativo a la longitud de la cadena más extensa. Esto facilita comparar resultados entre cadenas de tamaños diferentes.

## Heurística propuesta

El proceso implementado utiliza:

1. Eliminación de espacios externos mediante `strip()`.
2. Conversión a minúsculas mediante `lower()`.
3. Cálculo de la distancia de Levenshtein.
4. Normalización respecto de la longitud de la cadena más extensa.
5. Presentación del resultado como porcentaje.

Una posible regla de decisión es:

| Similitud | Interpretación |
|---:|---|
| 90 % a 100 % | Coincidencia muy alta. |
| 75 % a menos de 90 % | Coincidencia probable; conviene revisar. |
| 50 % a menos de 75 % | Coincidencia débil. |
| Menos de 50 % | Cadenas probablemente diferentes. |

Estos umbrales son orientativos y deben calibrarse con datos reales del dominio.

## Complejidad

Sean `N` y `M` las longitudes de las cadenas.

### Distancia de Hamming

- **Tiempo: O(N).** Compara una vez cada posición.
- **Memoria adicional: O(1).** Solo mantiene un contador y las variables del recorrido.

### Distancia de Levenshtein

- **Tiempo: O(N × M).** Se completa una matriz con `N × M` estados.
- **Memoria: O(N × M).** La implementación conserva la matriz completa.

### Similitud normalizada

- La normalización de las cadenas requiere O(N + M).
- El costo dominante es Levenshtein: O(N × M).

La memoria de Levenshtein puede optimizarse a O(min(N, M)) si solamente se conservan la fila actual y la anterior. La implementación actual conserva toda la matriz para mantener el algoritmo más directo.

## Estructura del código

| Función | Responsabilidad |
|---|---|
| `distancia_hamming` | Cuenta las posiciones diferentes y rechaza cadenas de distinta longitud. |
| `distancia_levenshtein` | Calcula la distancia mínima mediante programación dinámica. |
| `calcular_similitud_normalizada` | Normaliza las cadenas y convierte Levenshtein en un porcentaje. |
| `ejecutar_demostracion` | Ejecuta los casos predefinidos de los incisos. |
| `parsear_argumentos` | Procesa las opciones `--string1` y `--string2`. |
| `main` | Ejecuta una comparación personalizada o la demostración. |

## Incisos resueltos

### Inciso A — Distancia de Hamming

Se implementa `distancia_hamming` y se demuestra que:

- Una transposición puede contabilizarse como dos diferencias.
- Las cadenas de distinta longitud no son válidas para esta métrica.

### Inciso B — Distancia de Levenshtein

Se implementa mediante programación dinámica, considerando inserciones, eliminaciones y sustituciones.

### Inciso C — Pruebas con errores de escritura

Se incluyen casos como:

```text
"Horacio López" vs. "Oracio López"
```

La distancia obtenida es 1 porque debe eliminarse o insertarse una sola letra.

### Inciso D — Heurística de comparación

Se normalizan espacios externos y mayúsculas, se calcula Levenshtein y se expresa el resultado como porcentaje respecto de la cadena más larga.

## Notas

- Hamming requiere cadenas de igual longitud.
- Una transposición se contabiliza como dos sustituciones independientes tanto en Hamming como en la implementación estándar de Levenshtein.
- `strip()` elimina únicamente los espacios externos; no corrige espacios duplicados dentro de la cadena.
- `lower()` ignora diferencias entre mayúsculas y minúsculas, pero conserva diferencias de acentuación.
- Por ese motivo, `"Teoría"` y `"Teoria"` no se consideran idénticas.
- El porcentaje de similitud es una heurística derivada de Levenshtein, no una probabilidad estadística.
- Los umbrales de similitud deben ajustarse según el dominio y el costo de falsos positivos y falsos negativos.
- Las comillas protegen cadenas con espacios cuando se ingresan desde la terminal.
