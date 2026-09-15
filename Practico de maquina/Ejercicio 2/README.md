# Entropía empírica en imágenes (BMP vs. JPG)

## Descripción

Este programa analiza y compara una imagen en formato BMP con una imagen en formato JPG como secuencias de bytes y realiza las siguientes operaciones:

- Valida que los archivos existan y que sus extensiones sean `.bmp`, `.jpg` o `.jpeg`.
- Comprueba sus firmas binarias: `BM` para BMP y `FF D8` para JPG.
- Lee e imprime los principales campos de la cabecera BMP.
- Calcula la frecuencia relativa de aparición de cada byte posible (`0` a `255`), representada por `p_i`.
- Calcula la entropía empírica de Shannon: $H = -Σ p_i · log2(p_i)$
- Genera histogramas para comparar las distribuciones de probabilidad de ambos archivos.

Para un byte existen 256 símbolos posibles, por lo que la entropía máxima teórica es:

$H_max = log2(256) = 8 bits/símbolo$

El análisis se realiza sobre todos los bytes de los archivos, incluyendo las cabeceras, los metadatos y los datos de imagen. No se analizan solamente los píxeles.

El programa principal importa:

```python
from utils import (
    calcular_distribucion_bytes,
    calcular_entropia_shannon,
)
```

Y utiliza las funciones de la siguiente manera:

```python
dist_bmp = calcular_distribucion_bytes(path_bmp)
dist_jpg = calcular_distribucion_bytes(path_jpg)

entropia_bmp = calcular_entropia_shannon(dist_bmp)
entropia_jpg = calcular_entropia_shannon(dist_jpg)
```

## Ejecución

El programa recibe obligatoriamente la ruta de una imagen BMP mediante `-b` o `--bmp` y la ruta de una imagen JPG mediante `-j` o `--jpg`.

### Comparar una imagen BMP con una JPG

```bash
python main.py -b imagen.bmp -j imagen.jpg
```

También pueden utilizarse las opciones completas:

```bash
python main.py --bmp imagen.bmp --jpg imagen.jpg
```

### Mostrar la ayuda

```bash
python main.py --help
```

```text
usage: main.py [-h] -b BMP -j JPG

Análisis de entropía y distribución de información en imágenes BMP vs JPG.

options:
  -h, --help         show this help message and exit
  -b BMP, --bmp BMP  Ruta al archivo de imagen en formato BMP.
  -j JPG, --jpg JPG  Ruta al archivo de imagen en formato JPG.
```

Si se ejecuta sin alguno de los archivos, `argparse` muestra el modo de uso e informa cuál de los argumentos obligatorios falta.

## Ejemplo de salida

```text
--- CABECERA BMP ---
Firma: BM
Tamaño del archivo: 1440054 bytes
Ancho: 800 px
Alto: 600 px
Bits por píxel: 24
Tamaño de imagen (datos): 1440000 bytes
--------------------
Entropía BMP: 6.8421 bits/símbolo
Entropía JPG: 7.9354 bits/símbolo
```

Después de imprimir los resultados, el programa muestra dos histogramas:

- Distribución de probabilidad de los bytes del archivo BMP.
- Distribución de probabilidad de los bytes del archivo JPG.

Los valores son ilustrativos y dependen del contenido y de las características de las imágenes analizadas.

## Explicación teórica

Una imagen BMP suele almacenar los valores de los píxeles de forma directa, por lo que puede conservar patrones estadísticos como colores repetidos, fondos uniformes o regiones similares. Por este motivo, su distribución de bytes puede estar lejos de ser uniforme y su entropía empírica puede quedar por debajo de 8 bits por símbolo.

Una imagen JPG utiliza compresión con pérdida. De forma simplificada, divide la imagen en bloques, transforma sus valores, cuantifica los coeficientes obtenidos y codifica el resultado. Este proceso elimina información visual menos perceptible y reduce patrones redundantes.

Como resultado, los bytes de una imagen JPG suelen tener una distribución más uniforme y una entropía empírica de primer orden más cercana al máximo teórico de 8 bits por símbolo.

Sin embargo, una entropía alta no demuestra por sí sola que un archivo esté comprimido. Los datos cifrados o aleatorios también pueden presentar una distribución cercana a la uniforme. Además, esta medición analiza bytes individuales y no detecta dependencias entre secuencias de bytes.

## Complejidad

Sea `N` la suma de los tamaños de los archivos BMP y JPG:

- **Tiempo: O(N).** Cada byte se recorre una vez para actualizar su frecuencia.
- **Memoria: O(N).** La implementación actual utiliza `f.read()`, por lo que carga cada archivo completo en memoria.
- **Cálculo de entropía: O(256).** Cada distribución contiene 256 probabilidades, por lo que este costo es constante respecto de `N`.
- **Lectura de la cabecera: O(1).** Se leen únicamente los primeros 54 bytes del BMP.

Para archivos muy grandes sería conveniente procesar bloques, por ejemplo de 64 KB, y acumular las frecuencias sin mantener todo el contenido en memoria. Esa variante conservaría el tiempo O(N) y reduciría la memoria adicional a O(1), porque el alfabeto de bytes tiene un tamaño fijo.

## Estructura del código

| Función | Ubicación | Responsabilidad |
|---|---|---|
| `calcular_distribucion_bytes` | `utils.py` | Lee el archivo, cuenta los bytes y devuelve sus probabilidades. |
| `calcular_entropia_shannon` | `utils.py` | Calcula la entropía a partir de la distribución recibida. |
| `validar_archivo` | Programa principal | Comprueba que el archivo exista y delega la validación de su formato. |
| `validar_formato_bmp` | Programa principal | Comprueba que el archivo comience con la firma `BM`. |
| `validar_formato_jpg` | Programa principal | Comprueba que el archivo comience con el marcador `FF D8`. |
| `leer_header_bmp` | Programa principal | Lee y muestra los principales campos de la cabecera BMP. |
| `graficar_histogramas` | Programa principal | Muestra las distribuciones de probabilidad de BMP y JPG. |
| `parsear_argumentos` | Programa principal | Procesa los argumentos obligatorios `--bmp` y `--jpg`. |
| `main` | Programa principal | Coordina la validación, el análisis, los gráficos y el manejo de errores. |

## Notas

- Las extensiones se convierten a minúsculas, por lo que `.BMP`, `.JPG` y `.JPEG` también son aceptadas.
- Validar la firma binaria permite detectar archivos renombrados con una extensión incorrecta.
- La firma confirma el inicio esperado del formato, pero no garantiza que todo el archivo esté íntegro.
- La lectura fija de 54 bytes supone un BMP con una cabecera `BITMAPINFOHEADER` de 40 bytes.
- La entropía se calcula sobre todo el archivo y no exclusivamente sobre los datos de los píxeles.
- Para obtener una comparación significativa, las imágenes deberían representar el mismo contenido y tener dimensiones equivalentes.
- `plt.show()` mantiene abierta la ventana de gráficos hasta que el usuario la cierre, según el entorno utilizado.
- Es preferible importar explícitamente las funciones utilizadas desde `utils.py` en lugar de utilizar `from utils import *`.
