# Entropía Empírica en Archivos (Texto vs. Comprimidos)

Teoría de la Información — Práctico de Máquina 1, Ejercicio 3

## Descripción

Este programa lee un archivo arbitrario **byte por byte**, en un tiempo
**O(N)** (siendo N el tamaño del archivo), y calcula:

- La **frecuencia relativa** de aparición de cada byte (valores 0 a 255).
- La **entropía empírica** de Shannon:

  ```
  H = -Σ p_i · log2(p_i)
  ```

- El **rendimiento** (η = H / H_max) y la **redundancia** (R = 1 - η)
  respecto del máximo teórico de 8 bits/símbolo (256 valores de byte
  equiprobables → H_max = log2(256) = 8).

Permite analizar uno o varios archivos en la misma corrida y, si se le
pasan dos o más, imprime al final una tabla comparativa.

## Requisitos

- Python 3.8 o superior.
- No usa librerías externas (`os`, `math`, `argparse` y `collections` son
  parte de la librería estándar de Python) — no hace falta instalar nada.

## Instalación

1. Descargar `Ej3.py` y guardarlo en una carpeta.
2. Verificar que Python está instalado:

   ```bash
   python --version
   # o, en algunos sistemas:
   python3 --version
   ```

## Ejecución

El programa se ejecuta desde una terminal, pasándole la ruta de uno o más
archivos con el flag `-a` / `--archivos`.

### Analizar un solo archivo

```bash
python Ej3.py -a ejemplo_texto.txt
```

### Comparar dos (o más) archivos

Pensado especialmente para comparar un archivo de ejemplo_texto puro contra su
versión comprimida (`.zip`, `.rar`, etc.) de tamaño similar:

```bash
python Ej3.py -a ejemplo_texto.txt ejemplo_texto.zip
```

### Controlar cuántas filas se muestran en la tabla de frecuencias

Por defecto se muestran los 20 bytes más frecuentes. Se puede cambiar con
`-t` / `--top`:

```bash
python Ej3.py -a ejemplo_texto.txt ejemplo_texto.zip -t 10
```

### Ver todas las opciones

```bash
python Ej3.py --help
```

## Ejemplo de salida

```
Archivo: ejemplo_texto.txt
  Tamaño (bytes, N):       43400
  Símbolos distintos:      38 / 256
  Entropía H:              4.1752 bits/símbolo
  Entropía máxima:         8.0000 bits/símbolo
  Rendimiento (eta=H/Hmax):52.19 %
  Redundancia (R=1-eta):   47.81 %

    Byte   Símbolo   Frecuencia        p_i
  ------------------------------------------
      32                   7120     0.1641
      97         a         4280     0.0986
     101         e         4240     0.0977
     ...

Archivo: ejemplo_texto.zip
  Tamaño (bytes, N):       980
  Símbolos distintos:      231 / 256
  Entropía H:              6.6635 bits/símbolo
  Entropía máxima:         8.0000 bits/símbolo
  Rendimiento (eta=H/Hmax):83.29 %
  Redundancia (R=1-eta):   16.71 %
  ...

=======================================================
Comparación
=======================================================
  ejemplo_texto.txt                      H=4.1752 bits/símbolo   R=47.81%
  ejemplo_texto.zip                      H=6.6635 bits/símbolo   R=16.71%
```

## Explicación teórica

Un archivo de texto plano tiene patrones fuertes (letras frecuentes,
palabras repetidas, espacios), así que su distribución de bytes está lejos
de ser uniforme y su entropía queda muy por debajo de 8 bits/símbolo.

Un algoritmo de compresión (por ejemplo, DEFLATE en el caso del `.zip`,
que combina LZ77 + Huffman) detecta y elimina esos patrones repetitivos:
primero reemplaza secuencias repetidas por referencias (LZ77), y luego
asigna códigos cortos a lo que sigue siendo frecuente (Huffman). El
resultado es un flujo de bytes sin estructura explotable, donde todos los
valores tienden a aparecer con probabilidad similar — por eso su entropía
empírica se acerca al máximo teórico de 8 bits/símbolo. Esa cercanía al
máximo es la métrica de que ya no queda redundancia para seguir
comprimiendo con ese método.

## Estructura del código

| Función | Responsabilidad |
|---|---|
| `validar_archivo` | Verifica que el archivo exista antes de procesarlo |
| `calcular_distribucion_bytes` | Lee el archivo en bloques y cuenta ocurrencias de cada byte (O(N)) |
| `calcular_entropia` | Aplica la fórmula de Shannon sobre las frecuencias observadas |
| `imprimir_tabla_frecuencias` | Muestra la frecuencia relativa (p_i) de los bytes más comunes |
| `reportar` | Orquesta el análisis completo de un archivo e imprime el resumen |
| `parsear_argumentos` | Define y lee los argumentos de línea de comandos |
| `main` | Punto de entrada: recorre los archivos pedidos y muestra la comparación final |

## Autor / Materia

Teoría de la Información — Licenciatura en Ciencias de la Computación — 2026
