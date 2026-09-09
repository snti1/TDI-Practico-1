import argparse
import os
import numpy as np

def validar_archivo(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

def calcular_ic(path):
  frecuencias = np.zeros(256, dtype=int)
  sum = 0
  with open(path, "rb") as f:
    contenido = f.read()
    for byte in contenido:
      frecuencias[byte] += 1

  for f in frecuencias:
    sum += f * (f - 1)

  n = len(contenido)

  if n < 2:
      raise ValueError(f"El archivo {path} es demasiado pequeño para calcular el IC")
  
  return sum / (n * (n - 1))

## ARGUMENTOS DE LINEA DE COMANDOS
def parsear_argumentos():
  parser = argparse.ArgumentParser(
    description="El índice de coincidencia (IC) en criptografía mide la probabilidad de que dos letras elegidas al azar en un texto sean idénticas."
  )
  parser.add_argument(
    "-a", "--archivos",
    required=True,
    nargs="+",
    type=str,
    help="Ruta a uno o más archivos a analizar (ej: -a texto.txt texto.zip)."
  )
  return parser.parse_args()

def main():
  try:
    args = parsear_argumentos()
    print("## Cálculo de IC de archivos ##\n")

    resultados = {}
    for path in args.archivos:
      validar_archivo(path)
      ic = calcular_ic(path)
      _, ext = os.path.splitext(path)
      resultados[path] = ic
      print(f"IC archivo {ext.lower()} = {ic:.6f}")

    if len(resultados) >= 2:
      print("\n## Comparación ##")
      for path, ic in resultados.items():
        print(f"{os.path.basename(path):<20}{ic:.6f}")

  except Exception as e: 
    print(e)
if __name__ == "__main__":
  main()