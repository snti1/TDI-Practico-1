import json
import struct
import os

CAMPOS_BOOLEANOS = [
    "estudios_primarios", "estudios_secundarios", "estudios_universitarios",
    "vivienda_propia", "obra_social", "trabaja", "jubilado", "discapacidad"
]

# Formato Struct: '30s' (String 30 bytes), '30s' (String 30 bytes), 'I' (Unsigned Int 4 bytes), 'B' (Unsigned Char 1 byte)
FORMATO_REGISTRO = '30s 30s I B'
TAMANO_FIJO = struct.calcsize(FORMATO_REGISTRO)

ARCHIVO_JSON = "datos_personas_variable.json"
ARCHIVO_BINARIO = "datos_personas_fijo.bin"

def generar_datos_simulados(cantidad=20):
    """Genera una lista de diccionarios con datos simulados."""
    personas = []
    for i in range(1, cantidad + 1):
        persona = {
            "Apellido y Nombre": f"Usuario de Prueba {i}",
            "Direccion": f"Calle Ficticia {100 + i}",
            "DNI": 20000000 + i
        }
        
        # Asignación intercalada de cadenas "True"/"False" o "S"/"N"
        for j, campo in enumerate(CAMPOS_BOOLEANOS):
            if j % 2 == 0:
                persona[campo] = "True" if i % 2 == 0 else "False"
            else:
                persona[campo] = "S" if i % 3 == 0 else "N"
        
        personas.append(persona)
    return personas


def guardar_json(personas, nombre_archivo):
    """Inciso A: Almacena los datos en un archivo de texto de longitud variable (JSON)."""
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(personas, archivo, indent=4, ensure_ascii=False)
    print(f"[+] Datos de {len(personas)} personas guardados en JSON: {nombre_archivo}")


def guardar_binario_bitwise(personas, nombre_archivo):
    """Inciso B: Almacena los datos en binario empaquetando 8 booleanos en 1 byte."""
    with open(nombre_archivo, "wb") as archivo_bin:
        for persona in personas:
            # 1. Asegurar longitud fija de los strings
            nombre_bytes = persona["Apellido y Nombre"].ljust(30).encode('utf-8')[:30]
            direccion_bytes = persona["Direccion"].ljust(30).encode('utf-8')[:30]
            dni = persona["DNI"]
            
            # 2. Empaquetado Bitwise
            byte_empaquetado = 0
            for i, campo in enumerate(CAMPOS_BOOLEANOS):
                valor_actual = persona[campo]
                if valor_actual in ["True", "S"]:
                    byte_empaquetado |= (1 << i)  # Aplica máscara con operador OR
            
            # 3. Escribir estructura física en disco
            registro = struct.pack(FORMATO_REGISTRO, nombre_bytes, direccion_bytes, dni, byte_empaquetado)
            archivo_bin.write(registro)
            
    print(f"[+] Datos guardados en binario optimizado: {nombre_archivo}")
    print(f"    Cada registro ocupa exactamente {TAMANO_FIJO} bytes.")


def comparar_tamanos(arch_json, arch_bin):
    """Inciso C: Compara el peso en disco de ambos archivos."""
    tamano_json = os.path.getsize(arch_json)
    tamano_binario = os.path.getsize(arch_bin)
    ahorro = 100 - (tamano_binario / tamano_json * 100)
    
    print("\n=== COMPARATIVA DE ALMACENAMIENTO ===")
    print(f"Tamaño JSON (Variable):    {tamano_json} bytes")
    print(f"Tamaño BINARIO (Fijo):     {tamano_binario} bytes")
    print(f"Ahorro de espacio:         {ahorro:.2f}%")
    print("=====================================\n")


def leer_y_mostrar_json(nombre_archivo, limite=2):
    """Inciso D (parte 1): Lee y muestra registros desde el JSON."""
    print("=== DATOS RECUPERADOS DEL ARCHIVO JSON (TEXTO) ===")
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
        for i, persona in enumerate(datos[:limite]):
            print(f"\n[Registro JSON {i+1}]")
            print(f"Nombre: {persona['Apellido y Nombre']} | DNI: {persona['DNI']}")
            for campo in CAMPOS_BOOLEANOS:
                print(f"  - {campo}: {persona[campo]}")


def leer_y_desempaquetar_binario(nombre_archivo, limite=2):
    """Inciso D (parte 2): Lee el archivo binario y decodifica el byte de booleanos con AND."""
    print("\n" + "="*50)
    print("=== DATOS RECUPERADOS DEL ARCHIVO BINARIO ===")
    contador = 1
    
    with open(nombre_archivo, "rb") as archivo_bin:
        while True:
            bloque_bytes = archivo_bin.read(TAMANO_FIJO)
            if not bloque_bytes:
                break
            
            # Desempaquetar estructura
            nombre_bytes, direccion_bytes, dni, byte_empaquetado = struct.unpack(FORMATO_REGISTRO, bloque_bytes)
            
            # Limpiar strings
            nombre = nombre_bytes.decode('utf-8').strip()
            
            if contador <= limite:
                print(f"\n[Registro BINARIO {contador}]")
                print(f"Nombre: {nombre} | DNI: {dni}")
                print(f"Byte en memoria: {bin(byte_empaquetado)} ({byte_empaquetado} en decimal)")
                
                # Desempaquetado Bitwise con AND
                for i, campo in enumerate(CAMPOS_BOOLEANOS):
                    mascara = (1 << i)
                    bit_encendido = (byte_empaquetado & mascara) != 0
                    respuesta = "Sí" if bit_encendido else "No"
                    print(f"  - {campo}: {respuesta}")
            
            contador += 1
            
    print(f"\n[i] Se procesaron exitosamente {contador - 1} registros del archivo binario.")

if __name__ == "__main__":
    # 1. Generación de los datos base
    lista_personas = generar_datos_simulados(20)
    
    # 2. Escritura en ambos formatos
    guardar_json(lista_personas, ARCHIVO_JSON)
    guardar_binario_bitwise(lista_personas, ARCHIVO_BINARIO)
    
    # 3. Comparativa de tamaño físico
    comparar_tamanos(ARCHIVO_JSON, ARCHIVO_BINARIO)
    
    # 4. Verificación de lectura (limitada a 2 en pantalla para no saturar la consola)
    leer_y_mostrar_json(ARCHIVO_JSON, limite=2)
    leer_y_desempaquetar_binario(ARCHIVO_BINARIO, limite=2)