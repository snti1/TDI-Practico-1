# Análisis de Información en Señales de Audio (Formato WAV)
El formato WAV sin compresión (PCM) almacena las muestras de audio de forma secuencial. El objetivo de este ejercicio es analizar la cantidad de información real que transporta una señal de audio.
Desarrollar una aplicación de software que analice la distribución estadística de la información y la estructura interna de archivos de audio crudos y comprimidos. Se recomienda utilizar un archivo .wav y un archivo .mp3 que contengan exactamente la misma pista de audio para realizar la comparativa.

- a. Carga y Validación: Solicitar la ruta de ambos archivos y validar programáticamente que las extensiones y/o los formatos correspondan efectivamente a WAV y MP3.
- b. Análisis de Cabecera (Manipulación de bytes): Para el archivo WAV, el programa debe leer y aislar la cabecera estándar (RIFF/WAVE) e imprimir por pantalla sus datos principales (por ejemplo: identificadores "RIFF" y "WAVE", tamaño del archivo, frecuencia de muestreo, etc.).
- c. Distribución de Probabilidades: Leer el contenido de ambos archivos byte por byte (valores del 0 al 255) y calcular la frecuencia relativa de aparición de cada símbolo para obtener su distribución de probabilidad ($p_i$).
- d. Histogramas: Generar y mostrar el gráfico del histograma de frecuencias para ambos archivos, permitiendo una comparación visual.
- e. Cálculo de Entropía: A partir de las probabilidades obtenidas, calcular la entropía empírica de ambas fuentes utilizando la fórmula de Shannon: $H = -\sum p_i\log_2(p_i)$
- f. Comparar los valores de entropía obtenidos y la forma de los histogramas. Explicar desde la Teoría de la Información por qué se produce esta diferencia radical entre un archivo de audio sin compresión y uno comprimido.

# Descripción
Este programa lee dos archivos de audio (WAV y MP3), calcula sus distribuciones de probabilidad ($p_i$). A partir de las probabilidades obtenidas, 
calcula la entropía empírica de ambas fuentes utilizando la fórmula de Shannon y genera histogramas de frecuencias.

fórmula de Shannon: $H = -\sum p_i\log_2(p_i)$

## Uso
Para utilizarlo, se ejecuta desde la terminal:
```bash
python main.py -w audio.wav -m audio.mp3
```
### Parámetros
    -h, --help      show this help message and exit
    -w, --wav WAV   Ruta al archivo de audio en formato WAV.
    -m, --mp3 MP3   Ruta al archivo de audio en formato MP3.

## Ejemplo de salida
    ### Validacion de archivos ###
    Cabecera de archivo MP3: b'ID3'
    Archivo MP3 validado correctamente.
    Cabecera de archivo WAV: b'RIFF\x92\x1c \x00WAVE'
    Archivo WAV validado correctamente.

    ### Analisis de cabecera de archivo WAV ###
      ChunkID: RIFF
      Tamaño archivo: 2104466
      Formato: WAVE
      Canales: 2
      Frecuencia de muestreo: 44100 Hz
      Bits por muestra: 16
      Tamaño de datos: 2104292 bytes

    ### Distribución de Probabilidades ###
    Entropia archivo WAV: 6.9594 bits/símbolo
    Entropia archivo MP3: 7.7278 bits/símbolo

![histograma](./histograma.png)

## Inciso f)

Los resultados obtenidos muestran una diferencia significativa entre la entropía y la distribución estadística de un archivo de audio WAV y su equivalente MP3. El archivo 
WAV presentó una entropía menor y un histograma con patrones más estructurados, reflejando la existencia de redundancias y correlaciones propias de la señal de audio 
original. En cambio, el archivo MP3 exhibió una entropía considerablemente mayor y un histograma más uniforme, indicando una distribución de símbolos cercana a la aleatoria.

Desde la Teoría de la Información, esta diferencia se debe a que los algoritmos de compresión buscan eliminar redundancias estadísticas y perceptuales presentes en la señal 
original. En el caso del MP3, además de aplicar técnicas de codificación eficientes, se descartan componentes sonoras consideradas poco relevantes para la percepción humana 
mediante modelos psicoacústicos. Como consecuencia, los datos resultantes contienen menos patrones repetitivos y una distribución de probabilidades más uniforme.

Un histograma uniforme implica que los símbolos poseen probabilidades similares de ocurrencia, lo que incrementa la entropía y reduce la redundancia explotable. Por esta 
razón, un archivo MP3 ya comprimido resulta mucho más difícil de comprimir nuevamente, mientras que un archivo WAV conserva una cantidad importante de información redundante 
susceptible de ser aprovechada por algoritmos de compresión.

En síntesis, la mayor entropía observada en el MP3 es una evidencia de que el proceso de compresión ha concentrado la información relevante y eliminado redundancias, 
acercando la entropía empírica de la fuente codificada a su límite teórico superior.