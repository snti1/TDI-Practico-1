import math
import numpy as np

def calcular_entropia_shannon(distribucion):
  entropia = 0.0
  for p in distribucion:
      if p > 0:
          entropia -= p * math.log2(p)
  return entropia

def calcular_distribucion_bytes(path):
    frecuencias = np.zeros(256, dtype=int)
    
    with open(path, "rb") as f:
        contenido = f.read()
        for byte in contenido:
            frecuencias[byte] += 1

    total_bytes = len(contenido)
    distribucion = frecuencias / total_bytes
    return distribucion
