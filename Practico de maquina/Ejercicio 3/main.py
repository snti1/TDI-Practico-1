import sys
import math
from collections import Counter

BITS_MAXIMOS = 8  # log2(256), máximo teórico de un byte


def calcular_entropia(path: str):
    contador = Counter()
    n = 0
    with open(path, "rb") as f:  # abre el archivo en modo binario
        # lee en bloques de 64 KB en vez de todo de una vez, para no
        # cargar archivos enormes en memoria; cada byte se toca una
        # sola vez esto es lo que garantiza el O(N)
        for bloque in iter(lambda: f.read(65536), b""):
            contador.update(bloque)  # cuenta cuántas veces aparece cada byte (0..255)
            n += len(bloque)
    if n == 0:
        return 0.0, 0.0, 0, contador
    entropia = 0.0
    for frecuencia in contador.values():
        p_i = frecuencia / n  # frecuencia relativa (probabilidad empírica) del byte
        entropia -= p_i * math.log2(p_i)
    rendimiento = entropia / BITS_MAXIMOS
    redundancia = 1 - rendimiento
    return entropia, redundancia, n, contador

def imprimir_tabla_frecuencias(contador: Counter, n: int, top: int = 20):
    print(f"\n  {'Byte':>6} {'Símbolo':>9} {'Frecuencia':>12} {'p_i':>10}")
    print("  " + "-" * 42)
    mas_frecuentes = contador.most_common(top)
    for byte, frecuencia in mas_frecuentes:
        p_i = frecuencia / n
        # si el byte corresponde a un caracter ASCII imprimible, lo mostramos
        # como caracter; si no (bytes de control, binarios), mostramos su
        # valor hexadecimal
        simbolo = chr(byte) if 32 <= byte <= 126 else f"\\x{byte:02x}"
        print(f"  {byte:>6} {simbolo:>9} {frecuencia:>12} {p_i:>10.4f}")
    restantes = len(contador) - len(mas_frecuentes)
    if restantes > 0:
        print(f"  ... y {restantes} símbolos más (no mostrados)")

def reportar(path: str, top: int = 20):
    H, R, N, frecuencias = calcular_entropia(path)
    eta = (H / BITS_MAXIMOS) if BITS_MAXIMOS else 0.0
    print(f"\nArchivo: {path}")
    print(f"  Tamaño (bytes, N):       {N}")
    print(f"  Símbolos distintos:      {len(frecuencias)} / 256")
    print(f"  Entropía H:              {H:.4f} bits/símbolo")
    print(f"  Entropía máxima:         {BITS_MAXIMOS:.4f} bits/símbolo")
    print(f"  Rendimiento (eta=H/Hmax):{eta*100:.2f} %")
    print(f"  Redundancia (R=1-eta):   {R*100:.2f} %")
    imprimir_tabla_frecuencias(frecuencias, N, top=top)
    return H, R, N

def main():
    if len(sys.argv) < 2:
        print("Uso: python entropia_archivo.py archivo1 [archivo2 ...]")
        sys.exit(1)
    resultados = []
    for path in sys.argv[1:]:
        try:
            H, R, N = reportar(path)
            resultados.append((path, H, R, N))
        except FileNotFoundError:
            print(f"\nArchivo no encontrado: {path}")
    if len(resultados) >= 2:
        print("\n" + "=" * 55)
        print("Comparación")
        print("=" * 55)
        for path, H, R, N in resultados:
            print(f"  {path:30s} H={H:6.4f} bits/símbolo   R={R*100:5.2f}%")
        print(
            "\nInterpretación: cuanto más comprimido está un archivo, más "
            "cerca está su entropía empírica del máximo teórico (8 "
            "bits/símbolo) y más chica es su redundancia. Esto es "
            "esperable: un buen compresor elimina los patrones repetidos "
            "(la redundancia estadística) del archivo original, así que "
            "en la salida comprimida cada byte tiende a la equiprobabilidad "
            "y aporta la máxima información posible por símbolo."
        )

if __name__ == "__main__":
    main()