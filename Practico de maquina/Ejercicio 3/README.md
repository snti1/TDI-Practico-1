# Entropía empírica en archivos (texto vs. comprimidos)

**Teoría de la Información — Práctico de Máquina 1, Ejercicio 3**

## Descripción

Este programa analiza uno o más archivos como secuencias de bytes y calcula para cada uno:

- La frecuencia relativa de aparición de cada byte posible (`0` a `255`), representada por `p_i`.
- La entropía empírica de Shannon: $H = -Σ p_i · log2(p_i)$

- El rendimiento: $η = H / H_max$

- La redundancia: $R = 1 - η$

Para un byte existen 256 símbolos posibles, por lo que la entropía máxima teórica es:

$H_max = log2(256) = 8 bits/símbolo$

El programa permite analizar varios archivos en una misma ejecución. Para cada archivo muestra un resumen y una tabla con los bytes más frecuentes. Cuando se procesan dos o más archivos, también imprime una comparación final.

El programa principal importa:
```python
from utils import (
    calcular_distribucion_bytes,
    calcular_entropia_shannon,
)
```

Y las utiliza de la siguiente manera:

```python
distribucion = calcular_distribucion_bytes(path)
entropia = calcular_entropia_shannon(distribucion)
```

## Ejecución

Los archivos se pasan como argumentos posicionales. El parámetro opcional `--top` permite indicar cuántos bytes frecuentes se mostrarán.

### Analizar un archivo

```bash
python entropia_archivo.py ejemplo_texto.txt
```

### Comparar varios archivos

```bash
python entropia_archivo.py ejemplo_texto.txt texto.zip
```

También pueden analizarse formatos diferentes:

```bash
python entropia_archivo.py audio.wav audio.mp3 imagen.bmp imagen.jpg
```

### Cambiar la cantidad de bytes mostrados

Por defecto se muestran los 20 bytes más frecuentes:

```bash
python entropia_archivo.py ejemplo_texto.txt texto.zip --top 30
```

También puede utilizarse la forma abreviada:

```bash
python entropia_archivo.py ejemplo_texto.txt -t 10
```

### Mostrar la ayuda

```bash
python entropia_archivo.py --help
```
    usage: main.py [-h] [-t TOP] archivos [archivos ...]

    Calcula la distribución, entropía y redundancia de uno o más archivos.

    positional arguments:
      archivos       Archivos que se analizarán.

    options:
      -h, --help     show this help message and exit
      -t, --top TOP  Cantidad de símbolos que se mostrarán.

Si el programa se ejecuta sin archivos, `argparse` muestra el modo de uso e informa que falta el argumento obligatorio `archivos`.

## Ejemplo de salida

```text
Archivo: ejemplo_texto.txt
  Tamaño (bytes, N):         43400
  Símbolos distintos:        38 / 256
  Entropía H:                4.1752 bits/símbolo
  Entropía máxima:           8.0000 bits/símbolo
  Rendimiento (η = H/Hmax):  52.19 %
  Redundancia (R = 1 - η):   47.81 %

    Byte   Símbolo   Frecuencia        p_i
  ------------------------------------------
      32                 7120      0.1641
      97         a       4280      0.0986
     101         e       4240      0.0977
  ... y 18 símbolos más (no mostrados)

Archivo: texto.zip
  Tamaño (bytes, N):         980
  Símbolos distintos:        231 / 256
  Entropía H:                6.6635 bits/símbolo
  Entropía máxima:           8.0000 bits/símbolo
  Rendimiento (η = H/Hmax):  83.29 %
  Redundancia (R = 1 - η):   16.71 %

    Byte   Símbolo   Frecuencia        p_i
  ------------------------------------------
       0      \x00          128      0.1306
      15      \x0f           84      0.0857
     240      \xf0           83      0.0847
  ... y 211 símbolos más (no mostrados)

=================================================================
Comparación
=================================================================
ejemplo_texto.txt         N=     43400 H=4.1752 R=47.81%
texto.zip                 N=       980 H=6.6635 R=16.71%
```

Los valores son ilustrativos y dependen del contenido real de los archivos.

## Explicación teórica

Un archivo de texto suele contener patrones estadísticos fuertes: espacios frecuentes, letras repetidas y secuencias recurrentes. Por eso, su distribución de bytes normalmente está lejos de ser uniforme y su entropía empírica suele ser menor que 8 bits por símbolo.

Un algoritmo de compresión busca reducir esas regularidades. Por ejemplo, DEFLATE combina LZ77, que representa secuencias repetidas mediante referencias, con codificación Huffman, que asigna códigos más cortos a símbolos frecuentes.

Como resultado, los bytes de un archivo comprimido suelen presentar una distribución más uniforme y una entropía empírica de primer orden más cercana a 8 bits por símbolo.

Sin embargo, una entropía alta no demuestra por sí sola que un archivo esté comprimido. Los datos cifrados o generados aleatoriamente también pueden presentar una distribución cercana a la uniforme. Además, esta medición analiza bytes individuales y no detecta dependencias entre secuencias de bytes.

## Complejidad

Sea `N` el tamaño del archivo:

- **Tiempo: O(N).** Cada byte se recorre una vez para actualizar su frecuencia.
- **Memoria: O(N).** La implementación actual utiliza `f.read()`, por lo que carga el archivo completo en memoria.
- **Cálculo final: O(256).** La distribución y la entropía recorren un alfabeto fijo de 256 valores, lo que se considera constante respecto de `N`.

Para archivos muy grandes sería conveniente procesar bloques, por ejemplo de 64 KB, y acumular las frecuencias sin mantener todo el contenido en memoria. Esa variante conservaría el tiempo O(N) y reduciría la memoria adicional a O(1), porque el alfabeto tiene un tamaño fijo.

## Estructura del código

| Función | Ubicación | Responsabilidad |
|---|---|---|
| `calcular_distribucion_bytes` | `utils.py` | Lee el archivo, cuenta los bytes y devuelve sus probabilidades. |
| `calcular_entropia_shannon` | `utils.py` | Calcula la entropía a partir de la distribución recibida. |
| `validar_archivo` | Programa principal | Comprueba que el archivo exista y no esté vacío. |
| `obtener_frecuencias` | Programa principal | Obtiene las frecuencias absolutas necesarias para la tabla. |
| `imprimir_tabla_frecuencias` | Programa principal | Imprime los bytes más comunes y sus probabilidades. |
| `reportar` | Programa principal | Coordina el análisis y presenta los resultados de un archivo. |
| `parsear_argumentos` | Programa principal | Procesa los archivos y la opción `--top` mediante `argparse`. |
| `imprimir_comparacion` | Programa principal | Muestra la comparación cuando se analizaron varios archivos. |
| `main` | Programa principal | Controla la ejecución general y el manejo de errores. |

## Notas

- Los bytes imprimibles del rango ASCII `32-126` se muestran como caracteres.
- Los bytes no imprimibles se representan como `\xHH`, donde `HH` es su valor hexadecimal.
- De forma predeterminada se muestran los 20 bytes más frecuentes.
- Los archivos vacíos se rechazan para evitar una división por cero al calcular la distribución.
- Importar explícitamente las funciones de `utils.py` facilita conocer las dependencias del programa y evita colisiones de nombres.
