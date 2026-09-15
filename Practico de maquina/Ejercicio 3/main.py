import os
import argparse
from collections import Counter

os.sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from utils import (
    calcular_entropia_shannon,
    calcular_distribucion_bytes,
)


BITS_MAXIMOS = 8


def validar_archivo(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"No se encontró el archivo: {path}"
        )

    if os.path.getsize(path) == 0:
        raise ValueError(
            f"El archivo está vacío: {path}"
        )


def obtener_frecuencias(distribucion, total_bytes):
    """
    Reconstruye las frecuencias absolutas a partir de la
    distribución calculada en utils.py.
    """
    return Counter({
        byte: round(probabilidad * total_bytes)
        for byte, probabilidad in enumerate(distribucion)
        if probabilidad > 0
    })


def imprimir_tabla_frecuencias(
    contador,
    total_bytes,
    top=20,
):
    print(
        f"\n  {'Byte':>6} "
        f"{'Símbolo':>9} "
        f"{'Frecuencia':>12} "
        f"{'p_i':>10}"
    )

    print("  " + "-" * 42)

    for byte, frecuencia in contador.most_common(top):
        probabilidad = frecuencia / total_bytes

        simbolo = (
            chr(byte)
            if 32 <= byte <= 126
            else f"\\x{byte:02x}"
        )

        print(
            f"  {byte:>6} "
            f"{simbolo:>9} "
            f"{frecuencia:>12} "
            f"{probabilidad:>10.4f}"
        )

    restantes = len(contador) - min(top, len(contador))

    if restantes > 0:
        print(
            f"  ... y {restantes} símbolos más "
            "(no mostrados)"
        )


def reportar(path, top=20):
    validar_archivo(path)

    # Funciones reutilizadas directamente desde utils.py
    distribucion = calcular_distribucion_bytes(path)
    entropia = calcular_entropia_shannon(distribucion)

    total_bytes = os.path.getsize(path)

    frecuencias = obtener_frecuencias(
        distribucion,
        total_bytes,
    )

    rendimiento = entropia / BITS_MAXIMOS
    redundancia = 1 - rendimiento

    print(f"\nArchivo: {path}")
    print(f"  Tamaño (bytes, N):         {total_bytes}")
    print(
        f"  Símbolos distintos:        "
        f"{len(frecuencias)} / 256"
    )
    print(
        f"  Entropía H:                "
        f"{entropia:.4f} bits/símbolo"
    )
    print(
        f"  Entropía máxima:           "
        f"{BITS_MAXIMOS:.4f} bits/símbolo"
    )
    print(
        f"  Rendimiento (η = H/Hmax):  "
        f"{rendimiento * 100:.2f} %"
    )
    print(
        f"  Redundancia (R = 1 - η):   "
        f"{redundancia * 100:.2f} %"
    )

    imprimir_tabla_frecuencias(
        frecuencias,
        total_bytes,
        top,
    )

    return entropia, redundancia, total_bytes


def parsear_argumentos():
    parser = argparse.ArgumentParser(
        description=(
            "Calcula la distribución, entropía y redundancia "
            "de uno o más archivos."
        )
    )

    parser.add_argument(
        "archivos",
        nargs="+",
        help="Archivos que se analizarán.",
    )

    parser.add_argument(
        "-t",
        "--top",
        type=int,
        default=20,
        help="Cantidad de símbolos que se mostrarán.",
    )

    return parser.parse_args()


def main():
    args = parsear_argumentos()
    resultados = []

    if args.top <= 0:
        raise ValueError(
            "--top debe ser mayor que cero"
        )

    for path in args.archivos:
        try:
            entropia, redundancia, total = reportar(
                path,
                args.top,
            )

            resultados.append(
                (path, entropia, redundancia, total)
            )

        except (FileNotFoundError, ValueError) as error:
            print(f"\nError: {error}")

        except OSError as error:
            print(
                f"\nNo se pudo procesar '{path}': {error}"
            )

    if len(resultados) >= 2:
        print("\n" + "=" * 65)
        print("Comparación")
        print("=" * 65)

        for path, entropia, redundancia, total in resultados:
            print(
                f"{os.path.basename(path):25s} "
                f"N={total:10d} "
                f"H={entropia:6.4f} "
                f"R={redundancia * 100:6.2f}%"
            )


if __name__ == "__main__":
    main()