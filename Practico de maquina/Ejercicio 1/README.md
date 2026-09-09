# Análisis de Información en Señales de Audio (Formato WAV)
El formato WAV sin compresión (PCM) almacena las muestras de audio de forma secuencial. El objetivo de este ejercicio es analizar la cantidad de información real que transporta una señal de audio.
Desarrollar una aplicación de software que analice la distribución estadística de la información y la estructura interna de archivos de audio crudos y comprimidos. Se recomienda utilizar un archivo .wav y un archivo .mp3 que contengan exactamente la misma pista de audio para realizar la comparativa.

- a. Carga y Validación: Solicitar la ruta de ambos archivos y validar programáticamente que las extensiones y/o los formatos correspondan efectivamente a WAV y MP3.
- b. Análisis de Cabecera (Manipulación de bytes): Para el archivo WAV, el programa debe leer y aislar la cabecera estándar (RIFF/WAVE) e imprimir por pantalla sus datos principales (por ejemplo: identificadores "RIFF" y "WAVE", tamaño del archivo, frecuencia de muestreo, etc.).
- c. Distribución de Probabilidades: Leer el contenido de ambos archivos byte por byte (valores del 0 al 255) y calcular la frecuencia relativa de aparición de cada símbolo para obtener su distribución de probabilidad ($p_i$).
- d. Histogramas: Generar y mostrar el gráfico del histograma de frecuencias para ambos archivos, permitiendo una comparación visual.
- e. Cálculo de Entropía: A partir de las probabilidades obtenidas, calcular la entropía empírica de ambas fuentes utilizando la fórmula de Shannon: $H = -\sum p_i\log_2(p_i)$
- f. Comparar los valores de entropía obtenidos y la forma de los histogramas. Explicar desde la Teoría de la Información por qué se produce esta diferencia radical entre un archivo de audio sin compresión y uno comprimido.

# Instrucciones de uso 
