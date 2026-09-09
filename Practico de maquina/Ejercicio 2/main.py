import struct
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import argparse

## VALIDACION DE ARCHIVOS
def validar_archivo(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext == ".bmp":
        if not validar_formato_bmp(path):
            raise Exception("El archivo especificado no tiene una cabecera BMP válida.")
    elif ext in [".jpg", ".jpeg"]:
        if not validar_formato_jpg(path):
            raise Exception("El archivo especificado no tiene una cabecera JPG válida.")
    else:
        raise Exception(f"Extensión no soportada: {ext}")

def validar_formato_bmp(ruta):
    with open(ruta, "rb") as f:
        inicio = f.read(2)
    return inicio == b"BM"

def validar_formato_jpg(ruta):
    with open(ruta, "rb") as f:
        inicio = f.read(2)
    # Firma SOI (Start of Image) de JPG: 0xFF 0xD8
    return inicio == b"\xff\xd8"

## LECTURA DE HEADER BMP
def leer_header_bmp(path):
    with open(path, "rb") as f:
        cabecera = f.read(54)

    firma, tam_archivo, reservado1, reservado2, offset_data, \
    tam_header_info, ancho, alto, planos, bits_pixel, \
    compresion, tam_imagen, res_h, res_v, colores, colores_importantes = struct.unpack("<2sIHHIIiiHHIIiiII", cabecera)

    print("--- CABECERA BMP ---")
    print("Firma:", firma.decode('ascii', errors='ignore'))
    print("Tamaño del archivo:", tam_archivo, "bytes")
    print("Ancho:", ancho, "px")
    print("Alto:", alto, "px")
    print("Bits por píxel:", bits_pixel)
    print("Tamaño de imagen (datos):", tam_imagen, "bytes")
    print("--------------------")

## CÁLCULOS ESTADÍSTICOS Y ENTROPÍA
def calcular_distribucion_bytes(path):
    frecuencias = np.zeros(256, dtype=int)
    
    with open(path, "rb") as f:
        contenido = f.read()
        for byte in contenido:
            frecuencias[byte] += 1

    total_bytes = len(contenido)
    distribucion = frecuencias / total_bytes
    return distribucion

def calcular_entropia(distribucion):
    entropia = 0.0
    for p in distribucion:
        if p > 0:
            entropia -= p * math.log2(p)
    return entropia

## GRÁFICOS
def graficar_histogramas(dist_bmp, dist_jpg):
    bytes_eje = np.arange(256)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.bar(bytes_eje, dist_bmp, color='skyblue', width=1.0)
    plt.title("Distribución de Probabilidad - BMP")
    plt.xlabel("Valor de Byte (0-255)")
    plt.ylabel("Probabilidad")
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.subplot(1, 2, 2)
    plt.bar(bytes_eje, dist_jpg, color='salmon', width=1.0)
    plt.title("Distribución de Probabilidad - JPG")
    plt.xlabel("Valor de Byte (0-255)")
    plt.ylabel("Probabilidad")
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()

## PARSER DE ARGUMENTOS
def parsear_argumentos():
    parser = argparse.ArgumentParser(
        description="Análisis de entropía y distribución de información en imágenes BMP vs JPG."
    )
    parser.add_argument(
        "-b", "--bmp",
        required=True,
        type=str,
        help="Ruta al archivo de imagen en formato BMP."
    )
    parser.add_argument(
        "-j", "--jpg",
        required=True,
        type=str,
        help="Ruta al archivo de imagen en formato JPG."
    )
    return parser.parse_args()

def main():
    args = parsear_argumentos()
    path_bmp = args.bmp
    path_jpg = args.jpg

    try:
        # A. Validación de extensiones y firmas mágicas
        validar_archivo(path_bmp)

        validar_archivo(path_jpg)

        # B. Lectura e impresión del Header BMP
        leer_header_bmp(path_bmp)

        # C. Cálculo de distribuciones de frecuencia
        dist_bmp = calcular_distribucion_bytes(path_bmp)
        dist_jpg = calcular_distribucion_bytes(path_jpg)

        # E. Cálculo de entropía de Shannon
        entropia_bmp = calcular_entropia(dist_bmp)
        entropia_jpg = calcular_entropia(dist_jpg)

        print(f"Entropía BMP: {entropia_bmp:.4f} bits/símbolo")
        print(f"Entropía JPG: {entropia_jpg:.4f} bits/símbolo")

        # D. Gráficos comparativos
        graficar_histogramas(dist_bmp, dist_jpg)
    except Exception as e: 
        print(e)

if __name__ == "__main__":
    main()