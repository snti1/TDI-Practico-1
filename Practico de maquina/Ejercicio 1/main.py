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

  if ext == ".mp3":
    validar_formato_mp3(path)
  elif ext  == ".wav":
    validar_formato_wav(path)
  else:
    raise Exception(f"Extension no soportada: {ext}")

def validar_formato_wav(ruta):
  with open(ruta, "rb") as f:
      cabecera = f.read(12)
  return cabecera[0:4] == b"RIFF" and cabecera[8:12] == b"WAVE"

def validar_formato_mp3(ruta):
  with open(ruta, "rb") as f:
      inicio = f.read(3)
  return inicio == b"ID3" or inicio[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2")

## LECTURA DE HEADER
def leer_header_wav(path):
  with open(path, "rb") as f: # abrimos el archivo en modo read binary
      cabecera = f.read(44)

  riff, chunk_size, formato, fmt, tam_fmt, audio_fmt, canales, \
  frec_muestreo, byte_rate, block_align, bits_muestra, \
  data_id, tam_data = struct.unpack("<4sI4s4sIHHIIHH4sI", cabecera)

  print("ChunkID:", riff.decode())
  print("Tamaño archivo:", chunk_size)
  print("Formato:", formato.decode())
  print("Canales:", canales)
  print("Frecuencia de muestreo:", frec_muestreo, "Hz")
  print("Bits por muestra:", bits_muestra)
  print("Tamaño de datos:", tam_data, "bytes")

def calcular_distribucion_bytes(path):
  ...

def calcular_entropia(distribucion):
  ...

def graficar_histograma(distribucion, titulo):
  ...

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
  args = parsear_argumentos()
  path_wav = args.wav
  path_mp3 = args.mp3

  validar_archivo(path_mp3)
  validar_archivo(path_wav)

  leer_header_wav(path_wav)
  
  ...

if __name__ == "__main__":
  main()