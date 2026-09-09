# Entropía Empírica en Archivos (Texto vs. Comprimidos)

Teoría de la Información — Práctico de Máquina 1, Ejercicio 3

## Descripción

Este programa lee un archivo arbitrario **byte por byte**, en un tiempo
**O(N)** (siendo N el tamaño del archivo), y calcula:

- La **frecuencia relativa** de aparición de cada byte (valores 0 a 255) → p_i
- La **entropía empírica** de Shannon:

  ```
  H = -Σ p_i · log2(p_i)
  ```

- El **rendimiento** (η = H / H_max) y la **redundancia** (R = 1 - η)
  respecto del máximo teórico de 8 bits/símbolo (256 valores de byte
  equiprobables → H_max = log2(256) = 8).

Permite analizar uno o varios archivos en la misma corrida e imprime, para
cada uno, la tabla de frecuencias relativas de sus bytes más comunes. Si se
le pasan dos o más archivos, además muestra al final una tabla comparativa.

## Requisitos

- Python 3.8 o superior.
- No usa librerías externas (`sys`, `math` y `collections` son parte de la
  librería estándar de Python) — no hace falta instalar nada.

## Instalación

1. Descargar `entropia_archivo.py` y guardarlo en una carpeta.
2. Verificar que Python está instalado:

   ```bash
   python --version
   # o, en algunos sistemas:
   python3 --version
   ```

## Ejecución

El programa se ejecuta desde una terminal, pasándole la ruta de uno o más
archivos directamente como argumentos (sin flags).

### Analizar un solo archivo

```bash
python entropia_archivo.py texto.txt
```

### Comparar dos (o más) archivos

Pensado especialmente para comparar un archivo de texto puro contra su
versión comprimida (`.zip`, `.rar`, etc.) de tamaño similar:

```bash
python entropia_archivo.py texto.txt texto.zip
```

Se pueden pasar más de dos archivos; la tabla comparativa final se arma con
todos los que hayan podido leerse.

### Sin argumentos

Si se ejecuta sin pasarle ningún archivo, el programa solo imprime el modo
de uso y termina (no es un error de sintaxis, es el comportamiento
esperado):

```bash
python entropia_archivo.py
# Uso: python entropia_archivo.py archivo1 [archivo2 ...]
```

## Ejemplo de salida

```
Archivo: texto.txt
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
  ... y 18 símbolos más (no mostrados)

Archivo: texto.zip
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
  texto.txt                      H=4.1752 bits/símbolo   R=47.81%
  texto.zip                      H=6.6635 bits/símbolo   R=16.71%

Interpretación: cuanto más comprimido está un archivo, más cerca está
su entropía empírica del máximo teórico (8 bits/símbolo) y más chica es
su redundancia...
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

## Complejidad

El algoritmo es **O(N)**: cada byte del archivo se lee y se cuenta una
única vez, usando un diccionario de conteo (`Counter`) indexado por valor
de byte (0 a 255, un alfabeto de tamaño fijo). Como el alfabeto es
constante, el trabajo por cada byte es O(1), y el cálculo final de H
(sobre a lo sumo 256 frecuencias) también es O(1) — de ahí que el costo
total crezca linealmente con el tamaño del archivo y no más rápido.

## Estructura del código

| Función | Responsabilidad |
|---|---|
| `calcular_entropia` | Lee el archivo en bloques de 64 KB, cuenta ocurrencias de cada byte (O(N)) y aplica la fórmula de Shannon sobre las frecuencias observadas |
| `imprimir_tabla_frecuencias` | Muestra la frecuencia relativa (p_i) de los bytes más comunes, ordenados de mayor a menor |
| `reportar` | Orquesta el análisis completo de un archivo (llama a las dos funciones anteriores) e imprime el resumen |
| `main` | Punto de entrada: lee los argumentos de línea de comandos, recorre los archivos pedidos y muestra la comparación final |

## Notas

- Los bytes no imprimibles (fuera del rango ASCII 32-126) se muestran en
  la tabla como `\xHH` (su valor hexadecimal) en vez de un carácter, algo
  común al analizar archivos comprimidos o binarios.
- Por defecto la tabla de frecuencias muestra los 20 bytes más comunes de
  cada archivo (parámetro `top` de `reportar`/`imprimir_tabla_frecuencias`)
  para no saturar la salida cuando el archivo usa los 256 valores posibles.

## Autor / Materia

Teoría de la Información — Licenciatura en Ciencias de la Computación — 2026
