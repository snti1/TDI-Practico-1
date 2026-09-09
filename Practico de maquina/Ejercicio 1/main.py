import struct
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import argparse

# para poder importar el utils .....
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import *

## VALIDACION DE ARCHIVOS
def validar_archivo(path):
  if not os.path.isfile(path):
      raise FileNotFoundError(f"No se encontró el archivo: {path}")

  _, ext = os.path.splitext(path)

  if ext == ".mp3":
    if not validar_formato_mp3(path):
      raise Exception("El archivo especificado no tiene una cabecera MP3 válida.")
  elif ext  == ".wav":
    if not validar_formato_wav(path):
      raise Exception("El archivo especificado no tiene una cabecera WAV válida.")
  else:
    raise Exception(f"Extension no soportada: {ext}")

def validar_formato_wav(ruta):
  with open(ruta, "rb") as f:
      cabecera = f.read(12)
  print(f"Cabecera de archivo WAV: {cabecera}")
  return cabecera[0:4] == b"RIFF" and cabecera[8:12] == b"WAVE"

def validar_formato_mp3(ruta):
  with open(ruta, "rb") as f:
      cabecera = f.read(3)
  print(f"Cabecera de archivo MP3: {cabecera}")
  return cabecera == b"ID3" or cabecera[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2")

## LECTURA DE HEADER
def leer_header_wav(path):
  with open(path, "rb") as f: # abrimos el archivo en modo read binary
      cabecera = f.read(44)

  riff, chunk_size, formato, fmt, tam_fmt, audio_fmt, canales, \
  frec_muestreo, byte_rate, block_align, bits_muestra, \
  data_id, tam_data = struct.unpack("<4sI4s4sIHHIIHH4sI", cabecera)

  print("  ChunkID:", riff.decode())
  print("  Tamaño archivo:", chunk_size)
  print("  Formato:", formato.decode())
  print("  Canales:", canales)
  print("  Frecuencia de muestreo:", frec_muestreo, "Hz")
  print("  Bits por muestra:", bits_muestra)
  print("  Tamaño de datos:", tam_data, "bytes")

## GRÁFICOS
def graficar_histogramas(dist_wav, dist_mp3):
  bytes_eje = np.arange(256)

  plt.figure(figsize=(12, 5))

  plt.subplot(1, 2, 1)
  plt.bar(bytes_eje, dist_wav, color='skyblue', width=1.0)
  plt.title("Distribución de Probabilidad - BMP")
  plt.xlabel("Valor de Byte (0-255)")
  plt.ylabel("Probabilidad")
  plt.grid(True, linestyle='--', alpha=0.6)

  plt.subplot(1, 2, 2)
  plt.bar(bytes_eje, dist_mp3, color='salmon', width=1.0)
  plt.title("Distribución de Probabilidad - JPG")
  plt.xlabel("Valor de Byte (0-255)")
  plt.ylabel("Probabilidad")
  plt.grid(True, linestyle='--', alpha=0.6)

  plt.tight_layout()
  plt.show()

def parsear_argumentos():
  parser = argparse.ArgumentParser(
      description="Análisis de entropía y distribución de información en archivos de audio WAV vs MP3."
  )
  parser.add_argument(
      "-w", "--wav",
      required=True,
      type=str,
      help="Ruta al archivo de audio en formato WAV."
  )
  parser.add_argument(
      "-m", "--mp3",
      required=True,
      type=str,
      help="Ruta al archivo de audio en formato MP3."
  )
  return parser.parse_args()

def main():
  # a) Carga y Validación
  args = parsear_argumentos()
  path_wav = args.wav
  path_mp3 = args.mp3
  try: 
    print("\n### Validacion de archivos ###")
    validar_archivo(path_mp3)
    print(" Archivo MP3 validado correctamente.")
    validar_archivo(path_wav)
    print("Archivo WAV validado correctamente.")

    # b) Análisis de Cabecera (Manipulación de bytes)
    print("\n### Analisis de cabecera de archivo WAV ###")
    leer_header_wav(path_wav)

    # c) Distribución de Probabilidades
    print("\n### Distribución de Probabilidades ###")
    # print(" ## Archivo WAV ##")
    dist_wav = calcular_distribucion_bytes(path_wav)
    # print(dist_wav)

    # print(" ## Archivo MP3 ##")
    dist_mp3 = calcular_distribucion_bytes(path_mp3)
    # print(dist_mp3)

    
    # e) Cálculo de Entropía
    entropia_wav = calcular_entropia_shannon(dist_wav)
    entropia_mp3 = calcular_entropia_shannon(dist_mp3)

    print(f"Entropia archivo WAV: {entropia_wav:.4f} bits/símbolo")
    print(f"Entropia archivo MP3: {entropia_mp3:.4f} bits/símbolo")

    # d) Histogramas
    graficar_histogramas(dist_wav, dist_mp3)
  except Exception as e: 
    print(e)

if __name__ == "__main__":
  main()