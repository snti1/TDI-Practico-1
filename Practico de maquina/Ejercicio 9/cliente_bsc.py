import os
import socket
import struct
import random
import math

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import calcular_entropia_shannon as calcular_entropia_general

# ========================================================== # CONFIGURACIÓN DEL CLIENTE
# ========================================================== #
HOST = "127.0.0.1"
PUERTO = 5555

# ========================================================== # PROTOCOLO DE COMUNICACIÓN Y RED
# ========================================================== #
def recibir_exactamente(sock, cantidad):
    datos = bytearray()
    while len(datos) < cantidad:
        bloque = sock.recv(cantidad - len(datos))
        if not bloque:
            raise ConnectionError("Conexión cerrada por el servidor.")
        datos.extend(bloque)
    return bytes(datos)

def recibir_mensaje(sock):
    encabezado = recibir_exactamente(sock, 4)
    longitud = struct.unpack("!I", encabezado)[0]
    datos = recibir_exactamente(sock, longitud)
    return datos.decode("ascii")

def enviar_mensaje(sock, mensaje):
    datos = mensaje.encode("ascii")
    encabezado = struct.pack("!I", len(datos))
    sock.sendall(encabezado + datos)

# ============================= # FUNCIONES AUXILIARES Y MATEMÁTICAS 
# ============================= #
def texto_a_binario(texto):
    """
    Convierte una cadena de texto en su representación binaria de 8 bits por carácter.
    """
    return ''.join(format(ord(c), '08b') for c in texto)

def binario_a_texto(binario):
    """
    Convierte una cadena binaria (múltiplo de 8) de vuelta a texto ASCII.
    """
    caracteres = []
    for i in range(0, len(binario), 8):
        byte = binario[i:i+8]
        if len(byte) == 8:
            caracteres.append(chr(int(byte, 2)))
    return ''.join(caracteres)

def calcular_entropia_binaria(p):
    """
    Calcula la entropía de Shannon H(p) = -p*log2(p) - (1-p)*log2(1-p)
    """
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)

# ========================================================== # FASE 1: EXPERIMENTACIÓN EMPÍRICA Y BER
# ========================================================== #
def ejecutar_fase1(sock):
    print("\n" + "="*65)
    print(" FASE 1: TRANSMISIÓN Y TASA DE ERROR EMPÍRICA (BER)")
    print("="*65)

    magnitudes = [100, 10000, 1000000]
    ber_estimado = 0.0

    for N in magnitudes:
        # Generar trama aleatoria sintética de N bits
        trama_original = "".join(random.choice("01") for _ in range(N))
        
        # Enviar trama a través del socket TCP
        enviar_mensaje(sock, trama_original)
        trama_recibida = recibir_mensaje(sock)

        # Contar errores bit a bit
        errores = sum(1 for b_orig, b_rec in zip(trama_original, trama_recibida) if b_orig != b_rec)
        ber = errores / N
        ber_estimado = ber  # Conservamos la estimación de la trama más grande

        print(f"[*] Trama de {N:10,d} bits -> Errores detectados: {errores:7,d} | BER = {ber:.6f}")

    
    # Prueba con texto visual
    print("\n" + "-"*65)
    print(" EFECTO VISUAL DEL RUIDO DEL CANAL EN UN TEXTO")
    print("-"*65)
    frase_original = "Teoría de la Información 2026 - Licenciatura en Ciencias de la Computación"
    binario_original = texto_a_binario(frase_original)
    
    enviar_mensaje(sock, binario_original)
    binario_recibido = recibir_mensaje(sock)
    frase_alterada = binario_a_texto(binario_recibido)

    print(f"Texto Original : {frase_original}")
    print(f"Texto Recibido : {frase_alterada}")
    
    return ber_estimado, binario_original, binario_recibido

# ========================================================== # FASE 2: MODELADO MATEMÁTICO Y CAPACIDAD DEL CANAL
# ========================================================== #
def ejecutar_fase2(p_estimada, x_binario, y_binario):
    print("\n" + "="*65)
    print(" FASE 2: MODELADO MATEMÁTICO Y CAPACIDAD DEL CANAL")
    print("="*65)

    # 1. Matriz del Canal P(Y|X)
    print("\n1. MATRIZ DEL CANAL P(Y|X) (Binario Simétrico):")
    p = p_estimada
    q = 1.0 - p
    print(f"   P(Y=0|X=0) = {q:.6f}    P(Y=1|X=0) = {p:.6f}")
    print(f"   P(Y=0|X=1) = {p:.6f}    P(Y=1|X=1) = {q:.6f}")

    # 2. Probabilidades de la Fuente P(X)
    total_bits = len(x_binario)
    count_0 = x_binario.count('0')
    count_1 = x_binario.count('1')
    px0 = count_0 / total_bits
    px1 = count_1 / total_bits

    print("\n2. PROBABILIDADES DE LA FUENTE DE ENTRADA P(X):")
    print(f"   P(X=0) = {px0:.6f}")
    print(f"   P(X=1) = {px1:.6f}")

    # 3. Información Mutua I(X;Y)
    # Probabilidades de salida P(Y): P(y_j) = sum_i P(x_i) * P(y_j | x_i)
    py0 = px0 * q + px1 * p
    py1 = px0 * p + px1 * q

    H_Y = calcular_entropia_general([py0, py1])
    H_Y_dado_X = px0 * calcular_entropia_binaria(p) + px1 * calcular_entropia_binaria(p)
    I_XY = H_Y - H_Y_dado_X

    print("\n3. INFORMACIÓN MUTUA I(X;Y):")
    print(f"   H(Y)     = {H_Y:.6f} bits/símbolo (Entropía de salida)")
    print(f"   H(Y|X)   = {H_Y_dado_X:.6f} bits/símbolo (Ruido del canal)")
    print(f"   I(X;Y)   = {I_XY:.6f} bits/símbolo")

    # 4. Capacidad del Canal C
    # C = 1 - H(p) para un BSC
    H_p = calcular_entropia_binaria(p)
    C = 1.0 - H_p

    print("\n4. CAPACIDAD MÁXIMA DEL CANAL (C):")
    print(f"   H(p)     = {H_p:.6f} bits/símbolo")
    print(f"   C        = 1 - H(p) = {C:.6f} bits/símbolo")

    # 5. Análisis de Maximización
    porcentaje_alcanzado = (I_XY / C * 100.0) if C > 0 else 100.0
    print("\n5. ANÁLISIS DE MAXIMIZACIÓN:")
    print(f"   I(X;Y) / C = {porcentaje_alcanzado:.2f}% de la capacidad teórica máxima.")

    """ ===================================================================================
    ANÁLISIS DE MAXIMIZACIÓN Y JUSTIFICACIÓN DE RESULTADOS (FASE 2 - PASO 5) 
    ===================================================================================
    1. ¿Logró su mensaje maximizar la capacidad del canal? 
    SÍ. El mensaje transmitido logró 
    maximizar la capacidad del canal dentro del margen de tolerancia del 5% al 10% permitido por la 
    consigna.

    Detalle numérico y justificación con la cadena transmitida: 
    - Cadena enviada: "Teoría de la Información 2026 - Licenciatura en Ciencias de la Computación" 
    - Longitud en binario: 592 bits en total (326 ceros y 266 unos). 
    - Frecuencia relativa de la fuente P(X): 
    P(X=0) = 326 / 592 = 0.550676 (55.07%) 
    P(X=1) = 266 / 592 = 0.449324 (44.93%)}

    A pesar del leve sesgo hacia el '0' debido a la redundancia estadística natural del texto en 
    castellano codificado en ASCII de 8 bits, la distribución P(X) es prácticamente equiprobable (≈ 0.50).

    Esto resultó en: 
    - Entropía de Salida H(Y) = 0.994277 bits/símbolo (rozando el máximo teórico de 1 bit). 
    - Ruido del Canal H(Y|X) = H(p) = 0.330881 bits/símbolo (con p ≈ 0.060868). 
    - Información Mutua I(X;Y) = H(Y) - H(p) = 0.663396 bits/símbolo. 
    - Capacidad Máxima C = 1 - H(p) = 0.669119 bits/símbolo.

    Rendimiento Alcanzado: I(X;Y) / C = 99.14% de la capacidad teórica máxima. Al existir una diferencia de 
    solo un 0.86% respecto al 100% ideal, el mensaje aprovechó el canal a su máxima eficiencia práctica dentro del margen permitido.

    2. ¿Qué característica debería tener la trama de bits enviada para que I(X;Y) sea estrictamente igual a C (100.00%)? -&gt; Para
    que la Información Mutua I(X;Y) iguale a la Capacidad de Canal C al 100%, los símbolos de la fuente de entrada deben ser ESTRICTAMENTE EQUIPROBABLES: P(X=0) = P(X=1) = 0.500000.

    """

# ========================================================== # PROGRAMA PRINCIPAL
# ========================================================== #
def main():
    print("="*65)
    print(" CLIENTE TCP - SIMULACIÓN Y MODELADO MATEMÁTICO DE CANAL BSC")
    print("="*65)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PUERTO))
        print(f"[+] Conectado exitosamente al servidor BSC en {HOST}:{PUERTO}")

        # Fase 1
        p_estimada, x_binario, y_binario = ejecutar_fase1(sock)

        # Finalizar conexión limpiamente
        enviar_mensaje(sock, "SALIR")
        sock.close()

        # Fase 2
        ejecutar_fase2(p_estimada, x_binario, y_binario)

    except ConnectionRefusedError:
        print(f"[!] Error: No se pudo conectar al servidor en {HOST}:{PUERTO}.")
        print("    Asegúrese de ejecutar 'python3 servidor_bsc.py' en otra terminal antes de iniciar el cliente.")
    except Exception as e:
        print(f"[!] Ocurrió un error en la ejecución: {e}")
    

if __name__ == "__main__":
    main()
