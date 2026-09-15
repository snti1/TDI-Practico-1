# Práctico de Máquina 1 — Teoría de la Información

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

## Utilidades compartidas

Los ejercicios de entropía reutilizan funciones genéricas definidas en `utils.py`:

```python
from utils import (
    calcular_distribucion_bytes,
    calcular_entropia_shannon,
)
```

La distribución empírica de bytes se obtiene mediante:

```python
distribucion = calcular_distribucion_bytes(path)
```

La entropía se calcula a partir de esa distribución:

```python
entropia = calcular_entropia_shannon(distribucion)
```

Centralizar estas operaciones evita repetir la misma lógica en los análisis de audio, imágenes, texto y archivos comprimidos.

## Ejercicio 1 — Audio WAV vs. MP3

Este ejercicio compara una pista de audio sin compresión almacenada en WAV/PCM con su versión comprimida en MP3. Para que la comparación sea significativa, ambos archivos deben contener la misma pista.

La aplicación:

- Solicita las rutas de un archivo WAV y uno MP3.
- Valida sus extensiones y firmas binarias.
- Lee los primeros 44 bytes de la cabecera WAV estándar.
- Desempaqueta los campos mediante `struct.unpack`.
- Calcula la distribución de probabilidad de los bytes de ambos archivos.
- Calcula sus entropías empíricas.
- Genera histogramas comparativos.

Campos principales mostrados de la cabecera WAV:

- Identificador `RIFF`.
- Tamaño del archivo.
- Formato `WAVE`.
- Cantidad de canales.
- Frecuencia de muestreo.
- Bits por muestra.
- Tamaño del bloque de datos.

### Ejecución

```bash
python main.py -w audio.wav -m audio.mp3
```

Opciones:

```text
-w, --wav    Ruta al archivo de audio WAV.
-m, --mp3    Ruta al archivo de audio MP3.
```

## Ejercicio 2 — Imágenes BMP vs. JPG

Este ejercicio compara una imagen BMP con una versión JPG de la misma fotografía.

La aplicación:

- Valida las extensiones `.bmp`, `.jpg` y `.jpeg`.
- Comprueba la firma `BM` del archivo BMP.
- Comprueba el marcador SOI `FF D8` del archivo JPG.
- Lee los primeros 54 bytes del BMP.
- Imprime el tamaño, ancho, alto, profundidad de color y tamaño de los datos.
- Calcula las distribuciones de probabilidad y las entropías.
- Muestra histogramas comparativos.

### Ejecución

```bash
python main.py -b imagen.bmp -j imagen.jpg
```

Opciones:

```text
-b, --bmp    Ruta al archivo de imagen BMP.
-j, --jpg    Ruta al archivo de imagen JPG.
```

## Ejercicio 3 — Texto vs. archivo comprimido

Este ejercicio calcula la entropía empírica y la redundancia de archivos arbitrarios. La comparación propuesta utiliza un texto plano y su versión comprimida en ZIP o RAR.

La aplicación:

- Lee cada archivo como una secuencia de bytes.
- Calcula la distribución de los valores `0-255`.
- Calcula la entropía empírica.
- Calcula el rendimiento respecto de 8 bits por símbolo.
- Calcula la redundancia relativa.
- Muestra los bytes más frecuentes.
- Permite comparar varios archivos en una misma ejecución.

### Ejecución

```bash
python main.py ejemplo_texto.txt texto.zip
```

La cantidad de símbolos mostrados puede modificarse con `--top`:

```bash
python main.py ejemplo_texto.txt texto.zip --top 30
```

## Ejercicio 4 — Índice de coincidencia

El índice de coincidencia mide la probabilidad de que dos elementos seleccionados al azar sean iguales:

$IC = \frac{\sum_i f_i(f_i-1)}{N(N-1)}$

El programa debe calcular el IC sobre los mismos archivos analizados en el ejercicio 3 y comparar sus resultados con la entropía.

Valores de referencia proporcionados por la consigna:

- Texto en español: aproximadamente `0.074`.
- Texto aleatorio sobre 27 letras: aproximadamente `0.038`.

Un texto natural presenta una distribución desigual y conserva patrones estadísticos. Un archivo comprimido tiende a reducir esos patrones, aumentar su entropía y disminuir su índice de coincidencia.

## Ejercicio 5 — Almacenamiento y operaciones bitwise

Este ejercicio administra datos de 20 personas:

- Apellido y nombre.
- Dirección.
- DNI.
- Ocho campos booleanos.

Los mismos datos deben almacenarse de dos formas:

1. Archivo de longitud variable, como JSON o CSV, con booleanos representados como texto.
2. Archivo binario de longitud fija, empaquetando los ocho booleanos en un único byte.

Cada booleano ocupa una posición del byte:

```text
bit 7  bit 6  bit 5  bit 4  bit 3  bit 2  bit 1  bit 0
  B7     B6     B5     B4     B3     B2     B1     B0
```

El empaquetado utiliza operaciones OR y desplazamientos:

```python
byte_booleanos |= int(valor) << posicion
```

El desempaquetado utiliza desplazamiento y máscara:

```python
valor = bool((byte_booleanos >> posicion) & 1)
```

Finalmente, deben compararse los tamaños de ambos archivos y comprobarse que los registros puedan recuperarse correctamente.

## Ejercicio 6 — Distancias entre cadenas

El ejercicio compara dos cadenas utilizando:

- Distancia de Hamming.
- Distancia de Levenshtein.

La distancia de Hamming cuenta posiciones diferentes y requiere cadenas de igual longitud. No modela correctamente inserciones, eliminaciones ni desplazamientos.

La distancia de Levenshtein calcula la cantidad mínima de:

- Inserciones.
- Eliminaciones.
- Sustituciones.

Además de imprimir ambas distancias, la consigna requiere proponer una heurística para comparar texto, especialmente nombres con errores de escritura.

## Ejercicio 7 — Validación de CUIT/CUIL

Este ejercicio aplica un código de detección de errores basado en Módulo 11.

El programa debe:

1. Solicitar un CUIT o CUIL de 11 dígitos.
2. Separar los primeros 10 dígitos.
3. Calcular el dígito verificador esperado.
4. Compararlo con el último dígito ingresado.
5. Informar si el identificador es válido o inválido.

El dígito de control permite detectar muchas alteraciones y errores de tipeo, aunque no constituye un mecanismo criptográfico ni demuestra que el número esté asignado a una persona real.

## Ejercicio 8 — Capacidad de canal por búsqueda exhaustiva

El ejercicio trabaja con un canal discreto sin memoria que posee:

- Dos símbolos de entrada.
- Cuatro símbolos de salida.
- Una matriz de transición `P(Y|X)` de tamaño `2 × 4`.

El programa debe validar que cada fila de la matriz sume 1 y recorrer:

```text
P(X=0) = 0.00, 0.01, 0.02, ..., 1.00
P(X=1) = 1 - P(X=0)
```

En cada iteración debe calcular:

- Probabilidades de salida `P(Y)`.
- Entropía de salida `H(Y)`.
- Ruido del canal `H(Y|X)`.
- Información mutua `I(X;Y)`.

El mayor valor encontrado aproxima la capacidad del canal:

$C \approx \max I(X;Y)$

Como el incremento de búsqueda es `0.01`, el resultado es una aproximación discreta y no necesariamente el máximo analítico exacto.

## Ejercicio 9 — Canal Binario Simétrico mediante TCP

Este ejercicio simula un Canal Binario Simétrico o BSC mediante una arquitectura cliente-servidor.

### Fase 1 — Simulación empírica

El cliente debe:

- Conectarse al servidor mediante TCP.
- Generar tramas aleatorias de diferentes tamaños.
- Enviar las tramas usando el protocolo de longitud de 4 bytes.
- Recibir las secuencias alteradas por el canal.
- Comparar cada bit transmitido con el recibido.
- Calcular la tasa empírica de error o BER.
- Analizar su convergencia mediante la Ley de los Grandes Números.
- Convertir una frase a binario, transmitirla y reconstruir el texto recibido.

La tasa de error se calcula como:

$BER = \frac{\text{bits erróneos}}{\text{bits transmitidos}}$

### Fase 2 — Modelo matemático

A partir de la trama enviada y la probabilidad de error del BSC, el programa debe calcular:

- Matriz de transición.
- Probabilidades empíricas de entrada.
- Información mutua de la transmisión.
- Capacidad teórica del canal.
- Diferencia entre la información mutua observada y la capacidad.

Para un BSC con probabilidad de error `p`:

$C = 1 - H_2(p)$

donde:

$H_2(p) = -p\log_2(p) - (1-p)\log_2(1-p)$

La capacidad se alcanza cuando los bits de entrada son equiprobables.

## Complejidad

| Ejercicio | Complejidad principal | Observación |
|---|---:|---|
| WAV vs. MP3 | O(N) | Recorre los bytes de ambos archivos. |
| BMP vs. JPG | O(N) | Recorre los bytes de ambas imágenes. |
| Texto vs. comprimido | O(N) | Cuenta cada byte del archivo. |
| Índice de coincidencia | O(N) | Cuenta frecuencias y recorre un alfabeto finito. |
| Empaquetado bitwise | O(P) | Procesa una cantidad `P` de personas; la consigna usa 20. |
| Hamming | O(L) | Compara posiciones de cadenas de longitud `L`. |
| Levenshtein | O(M·N) | Usa programación dinámica para cadenas de longitudes `M` y `N`. |
| Validación CUIT/CUIL | O(1) | Procesa siempre 11 dígitos. |
| Capacidad de canal | O(101) | Evalúa 101 distribuciones y una matriz fija de `2 × 4`. |
| Cliente BSC | O(B) | Procesa cada uno de los `B` bits transmitidos. |

Las funciones actuales de distribución utilizan `f.read()`, por lo que cargan cada archivo completo en memoria. Esto implica O(N) de memoria. Una implementación por bloques conservaría el tiempo O(N) y reduciría la memoria adicional a O(1), dado que el arreglo de frecuencias tiene siempre 256 posiciones.

## Validaciones importantes

- Rechazar rutas que no correspondan a archivos existentes.
- Evitar calcular distribuciones sobre archivos vacíos.
- Validar tanto las extensiones como las firmas binarias cuando el formato lo permita.
- Verificar el tamaño mínimo antes de desempaquetar una cabecera.
- Validar que las probabilidades pertenezcan al intervalo `[0,1]`.
- Validar que cada fila de una matriz de transición sume 1, considerando una tolerancia para errores de punto flotante.
- Rechazar cadenas de distinta longitud antes de aplicar Hamming.
- Validar que CUIT/CUIL contenga exactamente 11 dígitos.
- Verificar que las tramas del BSC contengan únicamente `0` y `1`.
- En TCP, recibir exactamente la cantidad de bytes declarada por el encabezado.

## Interpretación general

Los primeros ejercicios muestran que el tamaño físico de un archivo no equivale directamente a su información útil. Los formatos sin compresión suelen conservar patrones estadísticos y redundancia, mientras que los formatos comprimidos tienden a producir distribuciones de bytes más uniformes.

Los ejercicios de empaquetado, comparación de cadenas y dígitos verificadores muestran cómo la representación de los datos afecta el almacenamiento y la detección de errores.

Los últimos ejercicios trasladan estos conceptos a canales de comunicación: la información recibida depende del ruido, de la distribución de entrada y de la capacidad máxima del canal. Las simulaciones permiten comparar esos resultados teóricos con mediciones empíricas.

## Notas

- Las comparaciones WAV/MP3 y BMP/JPG deben utilizar el mismo contenido de origen.
- La entropía se calcula sobre todos los bytes del archivo, incluidas cabeceras y metadatos.
- Una entropía cercana a 8 bits por símbolo no prueba por sí sola que un archivo esté comprimido; los datos cifrados o aleatorios pueden mostrar un comportamiento similar.
- La validación mediante firma binaria comprueba el comienzo del formato, pero no garantiza la integridad completa del archivo.
- La cabecera WAV de 44 bytes corresponde al caso canónico PCM; algunos archivos incorporan bloques adicionales.
- La cabecera BMP de 54 bytes corresponde al formato clásico con `BITMAPINFOHEADER`; existen otras variantes.
- Los valores de capacidad obtenidos mediante búsqueda con paso `0.01` son aproximaciones.
- El BER empírico fluctúa más en tramas pequeñas y tiende a estabilizarse al aumentar la cantidad de bits.

## Autor / Materia

**Teoría de la Información — Licenciatura en Ciencias de la Computación — 2026**
