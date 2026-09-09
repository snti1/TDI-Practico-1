import os
import math
import argparse
from collections import Counter

BITS_MAXIMOS = 8  # log2(256), entropía máxima de un byte (256 valores equiprobables)

## VALIDACION DE ARCHIVOS
def validar_archivo(path):
  if not os.path.isfile(path):
    raise FileNotFoundError(f"No se encontró el archivo: {path}")

## LECTURA Y DISTRIBUCION DE BYTES (O(N), un solo recorrido del archivo)
def calcular_distribucion_bytes(path):
  contador = Counter()
  n = 0

  with open(path, "rb") as f:  # abrimos el archivo en modo read binary
    for bloque in iter(lambda: f.read(65536), b""):
      contador.update(bloque)
      n += len(bloque)

  return contador, n

## ENTROPIA DE SHANNON A PARTIR DE LAS FRECUENCIAS OBSERVADAS
def calcular_entropia(contador, n):
  entropia = 0.0
  for frecuencia in contador.values():
    p_i = frecuencia / n
    entropia -= p_i * math.log2(p_i)
  return entropia

## TABLA DE FRECUENCIA RELATIVA POR SIMBOLO (p_i)
def imprimir_tabla_frecuencias(contador, n, top=20):
  print(f"\n  {'Byte':>6} {'Símbolo':>9} {'Frecuencia':>12} {'p_i':>10}")
  print("  " + "-" * 42)

  mas_frecuentes = contador.most_common(top)
  for byte, frecuencia in mas_frecuentes:
    p_i = frecuencia / n
    simbolo = chr(byte) if 32 <= byte <= 126 else f"\\x{byte:02x}"
    print(f"  {byte:>6} {simbolo:>9} {frecuencia:>12} {p_i:>10.4f}")

  restantes = len(contador) - len(mas_frecuentes)
  if restantes > 0:
    print(f"  ... y {restantes} símbolos más (usá --top para ver más filas)")

## REPORTE COMPLETO DE UN ARCHIVO
def reportar(path, top_frecuencias=20):
  validar_archivo(path)

  contador, n = calcular_distribucion_bytes(path)

  if n == 0:
    print(f"\nArchivo: {path}")
    print("  El archivo está vacío.")
    return None

  entropia = calcular_entropia(contador, n)
  rendimiento = entropia / BITS_MAXIMOS
  redundancia = 1 - rendimiento

  print(f"\nArchivo: {path}")
  print(f"  Tamaño (bytes, N):       {n}")
  print(f"  Símbolos distintos:      {len(contador)} / 256")
  print(f"  Entropía H:              {entropia:.4f} bits/símbolo")
  print(f"  Entropía máxima:         {BITS_MAXIMOS:.4f} bits/símbolo")
  print(f"  Rendimiento (eta=H/Hmax):{rendimiento * 100:.2f} %")
  print(f"  Redundancia (R=1-eta):   {redundancia * 100:.2f} %")

  imprimir_tabla_frecuencias(contador, n, top=top_frecuencias)

  return entropia, redundancia, n

## ARGUMENTOS DE LINEA DE COMANDOS
def parsear_argumentos():
  parser = argparse.ArgumentParser(
    description="Entropía empírica y distribución de frecuencias de bytes en archivos arbitrarios (texto vs. comprimidos)."
  )
  parser.add_argument(
    "-a", "--archivos",
    required=True,
    nargs="+",
    type=str,
    help="Ruta a uno o más archivos a analizar (ej: -a texto.txt texto.zip)."
  )
  parser.add_argument(
    "-t", "--top",
    type=int,
    default=20,
    help="Cantidad de símbolos más frecuentes a mostrar en la tabla (default: 20)."
  )
  return parser.parse_args()

def main():
  args = parsear_argumentos()

  resultados = []
  for path in args.archivos:
    resultado = reportar(path, top_frecuencias=args.top)
    if resultado is not None:
      resultados.append((path, *resultado))

  if len(resultados) >= 2:
    print("\n" + "=" * 55)
    print("Comparación")
    print("=" * 55)
    for path, entropia, redundancia, n in resultados:
      print(f"  {path:30s} H={entropia:6.4f} bits/símbolo   R={redundancia * 100:5.2f}%")

if __name__ == "__main__":
  main()