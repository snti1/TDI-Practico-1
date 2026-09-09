# Eficiencia de Almacenamiento y Empaquetado a Nivel de Bits (Bitwise)

Teoría de la Información — Práctico de Máquina 1, Ejercicio 5

## Descripción

Este programa gestiona los datos de **20 personas** y permite almacenarlos en dos formatos diferentes:

* Un archivo de **texto de longitud variable**, utilizando formato JSON.
* Un archivo **binario de longitud fija**, optimizado mediante el empaquetamiento de los 8 campos booleanos en **un único byte por persona**.

Para cada persona se almacenan los siguientes datos:

* Apellido y Nombre
* Dirección
* DNI
* 8 campos booleanos:

  * Estudios primarios
  * Estudios secundarios
  * Estudios universitarios
  * Vivienda propia
  * Obra social
  * Trabaja
  * Jubilado
  * Discapacidad

El programa realiza además una comparación del tamaño físico de ambos archivos y permite recuperar los registros almacenados desde cualquiera de los dos formatos.

El objetivo es demostrar el impacto que tiene la elección de una estructura de codificación adecuada sobre la **eficiencia de almacenamiento**, especialmente cuando se trabaja con grandes cantidades de datos.

## Requisitos

* Python 3.8 o superior.
* No utiliza librerías externas. `json`, `struct` y `os` forman parte de la biblioteca estándar de Python.

## Instalación

1. Descargar el archivo `.py` y guardarlo en una carpeta.
2. Verificar que Python está instalado:

```bash
python --version
# o, en algunos sistemas:
python3 --version
```

3. No es necesario instalar ninguna dependencia adicional.

## Ejecución

El programa se ejecuta directamente desde una terminal:

```bash
python nombre_del_programa.py
```

o, dependiendo del sistema:

```bash
python3 nombre_del_programa.py
```

Al ejecutarlo se generan automáticamente **20 registros simulados** y se realizan las siguientes operaciones:

1. Generación de los datos.
2. Almacenamiento en JSON.
3. Almacenamiento en binario de longitud fija.
4. Comparación del tamaño de ambos archivos.
5. Lectura y muestra de los primeros registros almacenados en JSON.
6. Lectura y desempaquetado de los primeros registros del archivo binario.

## Archivos generados

El programa genera dos archivos:

```text
datos_personas_variable.json
datos_personas_fijo.bin
```

El archivo JSON almacena todos los campos de manera explícita como texto, mientras que el archivo binario utiliza una estructura fija y almacena los 8 valores booleanos en un solo byte.

## Formato del registro binario

Para el archivo binario se utiliza la siguiente estructura:

```python
FORMATO_REGISTRO = '30s 30s I B'
```

Cada registro ocupa exactamente **65 bytes**:

| Campo             |   Tamaño | Descripción                  |
| ----------------- | -------: | ---------------------------- |
| Apellido y Nombre | 30 bytes | Cadena de longitud fija      |
| Dirección         | 30 bytes | Cadena de longitud fija      |
| DNI               |  4 bytes | Entero sin signo (`I`)       |
| Booleanos         |   1 byte | Los 8 booleanos empaquetados |

Por lo tanto:

```text
30 + 30 + 4 + 1 = 65 bytes por persona
```

Para 20 personas, el archivo binario ocupa:

```text
20 × 65 = 1300 bytes
```

## Empaquetamiento Bitwise

Los 8 campos booleanos se almacenan dentro de un único byte.

Inicialmente el byte se encuentra en:

```python
byte_empaquetado = 0
```

Luego, para cada campo que posee valor verdadero (`"True"` o `"S"`), se activa el bit correspondiente:

```python
byte_empaquetado |= (1 << i)
```

Cada posición del byte representa uno de los campos:

| Bit | Campo                   |
| --: | ----------------------- |
|   0 | estudios_primarios      |
|   1 | estudios_secundarios    |
|   2 | estudios_universitarios |
|   3 | vivienda_propia         |
|   4 | obra_social             |
|   5 | trabaja                 |
|   6 | jubilado                |
|   7 | discapacidad            |

Por ejemplo, si los campos correspondientes a los bits 0, 2 y 5 son verdaderos:

```text
Bit:       7 6 5 4 3 2 1 0
Valor:     0 0 1 0 0 1 0 1
```

El byte resultante sería:

```text
00100101
```

y su valor decimal:

```text
37
```

De esta manera, los 8 valores booleanos ocupan exactamente **1 byte**, en lugar de almacenar cada valor como una cadena de caracteres.

## Desempaquetado Bitwise

Al leer el archivo binario, el byte que contiene los booleanos se recupera junto con el resto del registro.

Para determinar el estado de cada campo se utiliza una máscara:

```python
mascara = (1 << i)
```

Luego se aplica el operador AND:

```python
bit_encendido = (byte_empaquetado & mascara) != 0
```

Si el resultado es distinto de cero, el bit correspondiente estaba encendido y el campo es verdadero.

Este proceso permite reconstruir los 8 valores booleanos originales a partir de un único byte.

## Comparación de almacenamiento

El programa obtiene el tamaño físico de cada archivo utilizando:

```python
os.path.getsize()
```

y calcula el porcentaje de ahorro mediante:

```text
Ahorro = 100 - (Tamaño_binario / Tamaño_JSON × 100)
```

La salida tendrá una estructura similar a:

```text
=== COMPARATIVA DE ALMACENAMIENTO ===
Tamaño JSON (Variable):     XXXX bytes
Tamaño BINARIO (Fijo):      1300 bytes
Ahorro de espacio:          XX.XX%
=====================================
```

El tamaño exacto del archivo JSON puede variar debido a la representación textual de los datos, los nombres de los campos, los valores `"True"`, `"False"`, `"S"` y `"N"`, y el formato utilizado por `json.dump()`.

## Ejemplo de salida

```text
[+] Datos de 20 personas guardados en JSON: datos_personas_variable.json
[+] Datos guardados en binario optimizado: datos_personas_fijo.bin
    Cada registro ocupa exactamente 65 bytes.

=== COMPARATIVA DE ALMACENAMIENTO ===
Tamaño JSON (Variable):     XXXX bytes
Tamaño BINARIO (Fijo):      1300 bytes
Ahorro de espacio:          XX.XX%
=====================================

=== DATOS RECUPERADOS DEL ARCHIVO JSON (TEXTO) ===

[Registro JSON 1]
Nombre: Usuario de Prueba 1 | DNI: 20000001
  - estudios_primarios: False
  - estudios_secundarios: N
  - estudios_universitarios: False
  - vivienda_propia: N
  - obra_social: False
  - trabaja: N
  - jubilado: False
  - discapacidad: N

...

==================================================
=== DATOS RECUPERADOS DEL ARCHIVO BINARIO ===

[Registro BINARIO 1]
Nombre: Usuario de Prueba 1 | DNI: 20000001
Byte en memoria: 0b0 (0 en decimal)
  - estudios_primarios: No
  - estudios_secundarios: No
  - estudios_universitarios: No
  - vivienda_propia: No
  - obra_social: No
  - trabaja: No
  - jubilado: No
  - discapacidad: No

...

[i] Se procesaron exitosamente 20 registros del archivo binario.
```

## Explicación teórica

En el archivo JSON, los datos se almacenan utilizando una representación textual. Esto hace que los campos booleanos ocupen más espacio, ya que valores como:

```text
"True"
"False"
"S"
"N"
```

requieren varios caracteres, además de los nombres de los campos y la estructura propia del formato JSON.

En cambio, en el archivo binario los datos se almacenan de forma más compacta. Los campos de texto tienen una longitud fija y los 8 valores booleanos se representan mediante los **8 bits de un único byte**.

Esto permite reducir considerablemente el espacio utilizado.

El beneficio se vuelve especialmente importante cuando la cantidad de registros aumenta. Por ejemplo, una diferencia de algunos bytes por persona puede representar una reducción considerable cuando se almacenan miles, millones o incluso más registros.

La elección de una estructura de representación adecuada es, por lo tanto, fundamental en sistemas de alta escala, ya que puede disminuir el espacio utilizado en disco y también reducir la cantidad de datos que deben transferirse o procesarse.

## Complejidad

### Generación de datos

La función `generar_datos_simulados()` genera `N` personas y recorre los 8 campos booleanos de cada una.

La complejidad es:

```text
O(N × 8)
```

Como el número de campos booleanos es constante, se puede considerar:

```text
O(N)
```

### Escritura JSON

La función `guardar_json()` procesa los `N` registros para generar el archivo:

```text
O(N)
```

### Escritura binaria

La función `guardar_binario_bitwise()` procesa cada persona y sus 8 campos booleanos:

```text
O(N × 8) = O(N)
```

### Lectura binaria

La función `leer_y_desempaquetar_binario()` recorre todos los registros almacenados y analiza los 8 bits de cada uno:

```text
O(N × 8) = O(N)
```

Por lo tanto, el costo total del procesamiento crece linealmente con la cantidad de personas.

## Estructura del código

| Función                        | Responsabilidad                                                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| `generar_datos_simulados`      | Genera los datos de las 20 personas y asigna valores a los 8 campos booleanos                                  |
| `guardar_json`                 | Guarda los registros en un archivo JSON de longitud variable                                                   |
| `guardar_binario_bitwise`      | Genera registros binarios de longitud fija y empaqueta los 8 booleanos en un byte mediante operaciones Bitwise |
| `comparar_tamanos`             | Obtiene y compara el tamaño físico de los archivos y calcula el porcentaje de ahorro                           |
| `leer_y_mostrar_json`          | Lee el archivo JSON y muestra los registros recuperados                                                        |
| `leer_y_desempaquetar_binario` | Lee los registros binarios y recupera los 8 booleanos utilizando máscaras y el operador AND                    |
| `main`                         | Ejecuta todas las etapas del programa en el orden correspondiente                                              |

## Incisos resueltos

### Inciso A — Archivo de longitud variable

Se almacenan los datos en:

```text
datos_personas_variable.json
```

Los valores booleanos se conservan como cadenas de caracteres, utilizando `"True"`, `"False"`, `"S"` o `"N"`.

### Inciso B — Archivo binario de longitud fija

Se utiliza:

```python
FORMATO_REGISTRO = '30s 30s I B'
```

Los 8 campos booleanos se empaquetan mediante operaciones Bitwise en exactamente **1 byte por persona**.

### Inciso C — Comparación

Se comparan los tamaños físicos de ambos archivos en bytes y se calcula el porcentaje de ahorro obtenido mediante el formato binario.

La conclusión es que una representación binaria compacta permite reducir el espacio requerido, especialmente cuando la cantidad de registros aumenta significativamente.

### Inciso D — Recuperación

El programa permite leer los dos archivos:

* El JSON se recupera mediante `json.load()`.
* El archivo binario se recupera mediante `struct.unpack()`.

En el caso del archivo binario, los 8 campos booleanos se reconstruyen utilizando operaciones Bitwise con el operador AND y máscaras.

## Notas

* El programa genera automáticamente **20 personas simuladas**.
* Los nombres y direcciones utilizados son datos ficticios.
* El archivo binario utiliza cadenas de hasta 30 bytes para nombre y dirección.
* Los registros binarios tienen una longitud fija de **65 bytes**.
* La lectura mostrada en pantalla está limitada a los primeros **2 registros** para evitar saturar la consola, aunque el programa procesa todos los registros del archivo binario.
* El tamaño final del JSON puede variar según la representación textual y el formato utilizado para almacenar los datos.

## Autor / Materia

Teoría de la Información — Licenciatura en Ciencias de la Computación — 2026
