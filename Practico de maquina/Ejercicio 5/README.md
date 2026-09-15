# Eficiencia de almacenamiento y empaquetado a nivel de bits (Bitwise)

**Teoría de la Información — Práctico de Máquina 1, Ejercicio 5**

## Descripción

Este programa gestiona los datos de **20 personas** y permite almacenarlos en dos formatos diferentes:

- Un archivo de texto de longitud variable en formato JSON.
- Un archivo binario de longitud fija, optimizado mediante el empaquetamiento de ocho campos booleanos en un único byte por persona.

Para cada persona se almacenan:

- Apellido y nombre.
- Dirección.
- DNI.
- Estudios primarios.
- Estudios secundarios.
- Estudios universitarios.
- Vivienda propia.
- Obra social.
- Trabaja.
- Jubilado.
- Discapacidad.

El programa compara el tamaño físico de ambos archivos y permite recuperar los registros almacenados desde cualquiera de los dos formatos.

El objetivo es demostrar el impacto de la representación elegida sobre la eficiencia de almacenamiento, especialmente al trabajar con grandes volúmenes de datos.

## Ejecución

El programa se ejecuta desde una terminal:

```bash
python main.py
```

Al ejecutarse realiza las siguientes operaciones:

1. Genera los datos de 20 personas.
2. Almacena los registros en formato JSON.
3. Almacena los mismos registros en un archivo binario de longitud fija.
4. Compara el tamaño de los archivos.
5. Lee y muestra registros recuperados desde el JSON.
6. Lee el archivo binario y desempaqueta sus campos booleanos.

## Archivos generados

```text
datos_personas_variable.json
datos_personas_fijo.bin
```

El archivo JSON almacena los campos explícitamente como texto. El archivo binario utiliza registros de longitud fija y representa los ocho valores booleanos mediante los ocho bits de un único byte.

## Formato del registro binario

La estructura utilizada es:

```python
FORMATO_REGISTRO = "30s 30s I B"
```

Cada registro ocupa 65 bytes:

| Campo | Tamaño | Descripción |
|---|---:|---|
| Apellido y nombre | 30 bytes | Cadena de longitud fija. |
| Dirección | 30 bytes | Cadena de longitud fija. |
| DNI | 4 bytes | Entero sin signo representado por `I`. |
| Booleanos | 1 byte | Ocho booleanos empaquetados. |

Por lo tanto:

```text
30 + 30 + 4 + 1 = 65 bytes por persona
```

Para 20 personas:

```text
20 × 65 = 1300 bytes
```

## Empaquetamiento bitwise

Los ocho campos booleanos se almacenan dentro de un único byte. Inicialmente:

```python
byte_empaquetado = 0
```

Para cada campo verdadero se activa el bit correspondiente:

```python
byte_empaquetado |= 1 << i
```

La asignación de bits es:

| Bit | Campo |
|---:|---|
| 0 | `estudios_primarios` |
| 1 | `estudios_secundarios` |
| 2 | `estudios_universitarios` |
| 3 | `vivienda_propia` |
| 4 | `obra_social` |
| 5 | `trabaja` |
| 6 | `jubilado` |
| 7 | `discapacidad` |

Por ejemplo, si los bits 0, 2 y 5 están activos:

```text
Bit:    7 6 5 4 3 2 1 0
Valor:  0 0 1 0 0 1 0 1
```

El byte resultante es:

```text
00100101₂ = 37₁₀
```

De esta manera, los ocho valores booleanos ocupan exactamente un byte en lugar de almacenarse como cadenas.

## Desempaquetado bitwise

Al leer el archivo binario se recupera el byte que contiene los booleanos. Para consultar un campo se construye una máscara:

```python
mascara = 1 << i
```

Luego se aplica el operador AND:

```python
bit_encendido = (byte_empaquetado & mascara) != 0
```

Si el resultado es distinto de cero, el bit se encontraba activo y el campo correspondiente es verdadero.

También puede obtenerse el valor desplazando el bit hasta la posición menos significativa:

```python
valor = bool((byte_empaquetado >> i) & 1)
```

## Comparación de almacenamiento

El tamaño físico de cada archivo se obtiene mediante:

```python
os.path.getsize(path)
```

El porcentaje de ahorro se calcula como:

$Ahorro = 100 - \left(\frac{Tamaño_{binario}}{Tamaño_{JSON}} \times 100\right)$

La salida presenta una estructura similar a:

```text
=== COMPARATIVA DE ALMACENAMIENTO ===
Tamaño JSON (Variable):     XXXX bytes
Tamaño BINARIO (Fijo):      1300 bytes
Ahorro de espacio:          XX.XX%
=====================================
```

El tamaño exacto del JSON puede variar por los nombres de las propiedades, la representación textual de los booleanos, los separadores y el formato aplicado por `json.dump()`.

## Ejemplo de salida

```text
[+] Datos de 20 personas guardados en JSON:
    datos_personas_variable.json

[+] Datos guardados en binario optimizado:
    datos_personas_fijo.bin
    Cada registro ocupa exactamente 65 bytes.

=== COMPARATIVA DE ALMACENAMIENTO ===
Tamaño JSON (Variable):     XXXX bytes
Tamaño BINARIO (Fijo):      1300 bytes
Ahorro de espacio:          XX.XX%
=====================================

=== DATOS RECUPERADOS DEL ARCHIVO JSON ===

[Registro JSON 1]
Nombre: Usuario de Prueba 1
DNI: 20000001

  - estudios_primarios: False
  - estudios_secundarios: N
  - estudios_universitarios: False
  - vivienda_propia: N
  - obra_social: False
  - trabaja: N
  - jubilado: False
  - discapacidad: N

=== DATOS RECUPERADOS DEL ARCHIVO BINARIO ===

[Registro BINARIO 1]
Nombre: Usuario de Prueba 1
DNI: 20000001
Byte en memoria: 0b0 (0 en decimal)

  - estudios_primarios: No
  - estudios_secundarios: No
  - estudios_universitarios: No
  - vivienda_propia: No
  - obra_social: No
  - trabaja: No
  - jubilado: No
  - discapacidad: No

[i] Se procesaron exitosamente 20 registros del archivo binario.
```

Los valores de tamaño y ahorro dependen de los datos generados y de la representación utilizada en el JSON.

## Explicación teórica

En el archivo JSON, los registros utilizan una representación textual. Los booleanos ocupan uno o varios caracteres mediante valores como:

```text
"True"
"False"
"S"
"N"
```

Además, JSON almacena los nombres de los campos, comillas, separadores y otros elementos estructurales.

En el archivo binario, los campos se almacenan de forma compacta y con longitud fija. Los ocho booleanos se representan mediante los ocho bits de un único byte, eliminando la repetición de sus representaciones textuales.

Esta reducción se vuelve relevante al aumentar la cantidad de registros. Ahorrar algunos bytes por persona puede representar una diferencia considerable cuando se procesan miles o millones de registros.

La representación binaria también puede reducir el volumen transferido y la cantidad de operaciones de entrada y salida. Como contrapartida, pierde legibilidad directa y requiere conocer exactamente el formato para interpretar los datos.

## Estructura del código

| Función | Responsabilidad |
|---|---|
| `generar_datos_simulados` | Genera los datos de las 20 personas y asigna los valores booleanos. |
| `guardar_json` | Almacena los registros en un archivo JSON de longitud variable. |
| `guardar_binario_bitwise` | Construye registros binarios fijos y empaqueta los ocho booleanos en un byte. |
| `comparar_tamanos` | Compara los tamaños físicos y calcula el porcentaje de ahorro. |
| `leer_y_mostrar_json` | Lee el JSON y muestra los registros recuperados. |
| `leer_y_desempaquetar_binario` | Lee los registros binarios y recupera los booleanos mediante máscaras. |
| `main` | Ejecuta las etapas del programa en el orden correspondiente. |

## Incisos resueltos

### Inciso A — Archivo de longitud variable

Los registros se almacenan en:

```text
datos_personas_variable.json
```

Los booleanos se conservan como cadenas, utilizando valores como `"True"`, `"False"`, `"S"` o `"N"`.

### Inciso B — Archivo binario de longitud fija

Se utiliza:

```python
FORMATO_REGISTRO = "30s 30s I B"
```

Los ocho campos booleanos se empaquetan mediante operaciones bitwise en exactamente un byte por persona.

### Inciso C — Comparación

Se comparan los tamaños físicos en bytes y se calcula el porcentaje de ahorro obtenido mediante la representación binaria.

La representación compacta reduce el espacio requerido, especialmente cuando la cantidad de registros aumenta.

### Inciso D — Recuperación

El archivo JSON se recupera mediante:

```python
json.load(archivo)
```

El archivo binario se recupera mediante:

```python
struct.unpack(FORMATO_REGISTRO, registro)
```

Los ocho booleanos se reconstruyen utilizando máscaras, desplazamientos y el operador AND.

## Notas

- El programa genera automáticamente 20 personas simuladas.
- Los nombres y direcciones utilizados son ficticios.
- El archivo binario reserva 30 bytes para el nombre y 30 para la dirección.
- Los registros binarios tienen una longitud fija de 65 bytes.
- La visualización se limita a los primeros dos registros para no saturar la consola, aunque todos los registros binarios son procesados.
- El tamaño final del JSON puede variar según los datos y el formato utilizado.
- Los textos deben codificarse y recortarse de forma segura antes de almacenarse en campos de 30 bytes.
- Para garantizar un formato binario portable entre plataformas conviene definir explícitamente el orden de bytes y la alineación, por ejemplo con `<30s30sIB`.
