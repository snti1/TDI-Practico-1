# Práctico de Máquina 1 - Teoría de la Información - Grupo 3

## Descripción

Este proyecto reúne las aplicaciones desarrolladas para el **Práctico de Máquina 1 de Teoría de la Información**. El trabajo aplica conceptos de cantidad de información, entropía, redundancia, codificación, detección de errores, distancia entre cadenas y capacidad de canales discretos.

Los ejercicios combinan análisis teórico con manipulación de archivos binarios, procesamiento estadístico, operaciones a nivel de bits, algoritmos de comparación de texto y comunicación mediante sockets TCP.

El práctico está compuesto por nueve ejercicios:

1. Análisis de información en señales de audio WAV y MP3.
2. Análisis de entropía, histogramas y estructura de imágenes BMP y JPG.
3. Entropía empírica en archivos de texto y archivos comprimidos.
4. Índice de coincidencia aplicado a texto y archivos comprimidos.
5. Eficiencia de almacenamiento y empaquetado de booleanos mediante operaciones bitwise.
6. Distancias de Hamming y Levenshtein entre cadenas.
7. Validación de CUIT/CUIL mediante Módulo 11.
8. Capacidad de un canal binario-cuaternario mediante búsqueda exhaustiva.
9. Simulación de un canal binario simétrico mediante sockets TCP.

## Objetivos

- Calcular distribuciones empíricas de probabilidad a partir de datos reales.
- Aplicar la fórmula de entropía de Shannon.
- Relacionar entropía, redundancia y compresión.
- Analizar estructuras binarias mediante lectura y desempaquetado de bytes.
- Comparar representaciones de longitud variable y fija.
- Aplicar operaciones bitwise para empaquetar información.
- Implementar métricas de distancia para detectar modificaciones en cadenas.
- Utilizar códigos de control para detectar errores.
- Calcular información mutua y capacidad de canal.
- Contrastar resultados teóricos con simulaciones empíricas.

## Estructura del practico
    Practico de maquina/
    ├── README.md
    ├── .gitignore
    ├── utils.py
    │
    ├── Ejercicio 1/
    │   ├── main.py
    │   ├── README.md
    │   ├── audio.wav
    │   └── audio.mp3
    │
    ├── Ejercicio 2/
    │   ├── main.py
    │   ├── README.md
    │   ├── imagen.bmp
    │   ├── imagen.jpg
    │   ├── imagen1.bmp
    │   └── imagen1.jpg
    │
    ├── Ejercicio 3/
    │   ├── main.py
    │   ├── README.md
    │   ├── ejemplo_texto.txt
    │   └── ejemplo_texto.zip
    │
    ├── Ejercicio 4/
    │   ├── main.py
    │   ├── README.md
    │   ├── ejemplo_texto.txt
    │   └── ejemplo_texto.zip
    │
    ├── Ejercicio 5/
    │   ├── main.py
    │   └── README.md
    │
    ├── Ejercicio 6/
    │   ├── main.py
    │   └── README.md
    │
    ├── Ejercicio 7/
    │   ├── main.py
    │   └── README.md
    │
    ├── Ejercicio 8/
    │   ├── main.py
    │   └── README.md
    │
    └── Ejercicio 9/
        ├── cliente_bsc.py
        ├── servidor_bsc.py
        └── README.md


## Utilidades compartidas

El módulo `utils.py` contiene las siguientes funciones genéricas:

| Función | Responsabilidad |
|---|---|
| `calcular_distribucion_bytes(path)` | Lee el archivo en modo binario, cuenta la aparición de cada byte y devuelve un arreglo de 256 probabilidades. |
| `calcular_entropia_shannon(distribucion)` | Recibe una distribución de probabilidades y calcula la entropía de Shannon. |

El programa principal no vuelve a definir estas funciones; solamente las importa:

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

## Fundamento teórico

### Cantidad de información

La información individual asociada a un símbolo de probabilidad $p_i$ se define como:

$I(x_i) = -\log_2(p_i)$

Un símbolo menos probable aporta más información que uno frecuente.

### Entropía de Shannon

La entropía representa la cantidad promedio de información generada por una fuente:

$H(X) = -\sum_i p_i\log_2(p_i)$

Cuando se analizan bytes, existen 256 símbolos posibles. Si todos son equiprobables:

$H_{max} = \log_2(256) = 8\ \text{bits/símbolo}$

### Rendimiento y redundancia

El rendimiento respecto de la entropía máxima se calcula como:

$\eta = \frac{H}{H_{max}}$

La redundancia relativa es:

$R = 1 - \eta$

Una distribución uniforme presenta entropía máxima. Una distribución con símbolos muy frecuentes y otros poco frecuentes posee mayor predictibilidad y menor entropía.

### Información mutua

La información mutua mide cuánta información proporciona la salida de un canal acerca de su entrada:

$I(X;Y) = H(Y) - H(Y|X)$

La capacidad de un canal discreto es el máximo valor de información mutua alcanzable al variar la distribución de entrada:

$C = \max_{P(X)} I(X;Y)$

## Requisitos

- Python instalado.
- NumPy.
- Matplotlib.

Instalación de las dependencias externas:

```bash
pip install numpy matplotlib
```

Los módulos `argparse`, `collections`, `math`, `os`, `socket`, `struct` y `sys` forman parte de la biblioteca estándar de Python.

## Ejecutar programas
```bash
cd '.\Practico de maquina\'
cd '.\Ejercicio X\'
python main.py ...
```

## Interpretación general

Los primeros ejercicios muestran que el tamaño físico de un archivo no equivale directamente a su información útil. Los formatos sin compresión suelen conservar patrones estadísticos y redundancia, mientras que los formatos comprimidos tienden a producir distribuciones de bytes más uniformes.

Los ejercicios de empaquetado, comparación de cadenas y dígitos verificadores muestran cómo la representación de los datos afecta el almacenamiento y la detección de errores.

Los últimos ejercicios trasladan estos conceptos a canales de comunicación: la información recibida depende del ruido, de la distribución de entrada y de la capacidad máxima del canal. Las simulaciones permiten comparar esos resultados teóricos con mediciones empíricas.

**Teoría de la Información - 2026**
