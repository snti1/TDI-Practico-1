# Entropía e Índice de Coincidencia en archivos

**Teoría de la Información — Práctico de Máquina 1, Ejercicio 4**

## Descripción

Este programa analiza uno o más archivos como secuencias de bytes y calcula para cada uno:

- La frecuencia relativa de aparición de cada byte posible (`0` a `255`), representada por `p_i`.
- La entropía empírica de Shannon: $H = -Σ p_i · log2(p_i)$
- El Índice de Coincidencia (IC): $IC = \dfrac{Σ_i f_i (f_i - 1)}{N (N - 1)}$

Para un byte existen 256 símbolos posibles, por lo que la entropía máxima teórica es:

$H_{max} = log2(256) = 8\ bits/símbolo$

De la misma forma, el IC de una fuente perfectamente uniforme (equiprobable) sobre 256 símbolos tiende a:

$IC_{uniforme} ≈ 1/256 ≈ 0{,}0039$

El programa permite analizar varios archivos en una misma ejecución. Para cada uno calcula ambas métricas y, al finalizar, imprime una tabla comparativa con los resultados de todos los archivos ingresados.

El programa principal importa:
```python
from utils import *
```

Y las utiliza de la siguiente manera:

```python
dist = calcular_distribucion_bytes(path)
entropia = calcular_entropia_shannon(dist)
```

El cálculo del IC se realiza en el propio programa principal, a partir de las frecuencias absolutas de cada byte:

```python
ic = calcular_ic(path)
```

## Ejecución

Los archivos se pasan mediante la flag `-a` / `--archivos`, que acepta uno o más valores.

### Analizar un archivo

```bash
python main.py -a ejemplo_texto.txt
```

### Comparar varios archivos

```bash
python main.py -a ejemplo_texto.txt texto.zip
```

> **Importante:** al usar `nargs="+"`, todos los archivos deben pasarse **después de una única flag `-a`**, separados por espacios. Repetir la flag (`-a archivo1 -a archivo2`) no acumula los valores, sino que el último `-a` sobrescribe a los anteriores.

### Mostrar la ayuda

```bash
python main.py --help
```
    usage: main.py [-h] -a ARCHIVOS [ARCHIVOS ...]

    El índice de coincidencia (IC) en criptografía mide la probabilidad de que
    dos letras elegidas al azar en un texto sean idénticas.

    options:
      -h, --help            show this help message and exit
      -a, --archivos ARCHIVOS [ARCHIVOS ...]
                            Ruta a uno o más archivos a analizar (ej: -a
                            texto.txt texto.zip).

Si el programa se ejecuta sin la flag `-a`, `argparse` muestra el modo de uso e informa que falta el argumento obligatorio `--archivos`.

## Ejemplo de salida

```text
## Cálculo de Entropía e IC de archivos ##

Archivo                                        Entropía             IC
----------------------------------------------------------------------
ejemplo_texto.txt                                4.1752       0.074249
ejemplo_texto.zip                                6.6635       0.033466
```

## Explicación teórica

Un archivo de texto suele contener patrones estadísticos fuertes: espacios frecuentes, letras repetidas y secuencias recurrentes debido. Por eso, su distribución de bytes normalmente está lejos de ser uniforme, lo que se traduce en una entropía empírica menor a 8 bits por símbolo y un IC más alto (mayor probabilidad de que dos bytes elegidos al azar coincidan).
Entropía e IC miden, desde ángulos distintos, la misma propiedad de la distribución de símbolos: mientras la entropía crece cuando la distribución se acerca a la uniformidad, el IC decrece en ese mismo caso. Por eso ambas métricas suelen variar en sentido inverso al comparar un archivo sin comprimir contra su versión comprimida.
Sin embargo, ni una entropía alta ni un IC bajo demuestran por sí solos que un archivo esté comprimido. Los datos cifrados o generados aleatoriamente también pueden presentar una distribución cercana a la uniforme. Además, esta medición analiza bytes individuales y no detecta dependencias entre secuencias de bytes.

## Estructura del código

| Función | Ubicación | Responsabilidad |
|---|---|---|
| `calcular_distribucion_bytes` | `utils.py` | Lee el archivo, cuenta los bytes y devuelve sus probabilidades. |
| `calcular_entropia_shannon` | `utils.py` | Calcula la entropía a partir de la distribución recibida. |
| `validar_archivo` | Programa principal | Comprueba que el archivo exista. |
| `calcular_ic` | Programa principal | Cuenta las frecuencias absolutas de cada byte y calcula el Índice de Coincidencia. |
| `mostrar_resultados` | Programa principal | Imprime la tabla comparativa de entropía e IC de todos los archivos analizados. |
| `parsear_argumentos` | Programa principal | Procesa la lista de archivos mediante `argparse`. |
| `main` | Programa principal | Controla la ejecución general, arma la lista de resultados y el manejo de errores. |