# Simulación y Análisis Teórico de un Canal Binario Simétrico (BSC) mediante Sockets TCP

Este proyecto implementa un sistema Cliente-Servidor para simular, modelar y analizar el comportamiento de un **Canal Binario Simétrico (BSC)** con ruido aleatorio, utilizando comunicaciones por **Sockets TCP** en Python y aplicando los principios fundamentales de la **Teoría de la Información y Entropía de Shannon**.

---

## 1. Descripción del Problema y Consignas

El ejercicio plantea modelar un canal de comunicaciones digital donde la probabilidad de error p permanece oculta en el servidor (actuando como una "caja negra"). El desarrollo se divide en dos fases consecutivas:

### Fase 1: Transmisión y Tasa de Error Empírica (BER)
1. **Conexión por Sockets TCP:** Implementar un cliente que establezca una conexión robusta con el servidor mediante un protocolo de enmarcado por longitud (cabecera binaria de 4 bytes en formato Big-Endian).
2. **Estimación Empírica de p:** Generar y transmitir tramas sintéticas aleatorias de bits con magnitudes crecientes (100, 10.000 y 1.000.000 de bits).
3. **Cálculo de BER:** Comparar bit a bit la trama transmitida con la recibida para obtener la **Tasa de Error de Bit** (\text{BER} = \frac{\text{errores}}{N}) y analizar su convergencia hacia la probabilidad de error p teórica en función de la **Ley de los Grandes Números**.
4. **Efecto Visual en Texto Plano:** Convertir una frase en texto plano a su representación binaria ASCII, transmitirla a través del canal ruidoso y reconvertir el mensaje recibido a texto para observar la degradación del mensaje.

### Fase 2: Modelado Matemático y Capacidad del Canal
1. **Matriz de Transición del Canal P(Y|X):** Construir la matriz estocástica del BSC con la probabilidad p estimada.
2. **Distribución de la Fuente de Entrada P(X):** Analizar las frecuencias relativas de ceros y unos en el mensaje enviado para determinar P(X=0) y P(X=1).
3. **Cálculo de la Información Mutua I(X;Y):** Determinar la entropía de salida H(Y), el ruido del canal H(Y|X) y la información mutua promedio I(X;Y) = H(Y) - H(Y|X).
4. **Capacidad Máxima del Canal (C):** Calcular el límite teórico máximo de transmisión confiable mediante C = 1 - H(p).
5. **Análisis de Maximización:** Evaluar el porcentaje de capacidad alcanzado (I(X;Y) / C) y responder teóricamente qué condiciones debe cumplir la fuente de entrada para maximizar I(X;Y).

---

## 2. Fundamentos Matemáticos y Teóricos

### 2.1. Canal Binario Simétrico (BSC)
Un BSC es un canal discreto sin memoria con alfabeto de entrada X \in \{0, 1\} y salida Y \in \{0, 1\}. Su comportamiento probabilístico está definido por la matriz de transición:

P(Y|X) = \begin{bmatrix} P(Y=0|X=0) & P(Y=1|X=0) \\ P(Y=0|X=1) & P(Y=1|X=1) \end{bmatrix} = \begin{bmatrix} 1-p & p \\ p & 1-p \end{bmatrix}

donde p es la probabilidad de que un bit se invierta durante la transmisión.

### 2.2. Probabilidades de Salida P(Y)
Mediante el **Teorema de la Probabilidad Total**, las probabilidades marginales de recibir cada símbolo en la salida son:

P(Y=0) = P(X=0)(1-p) + P(X=1)p
P(Y=1) = P(X=0)p + P(X=1)(1-p)

### 2.3. Entropía de Salida H(Y)
Mide la incertidumbre o proromedio de información recibido por símbolo:

H(Y) = - P(Y=0)\log_2 P(Y=0) - P(Y=1)\log_2 P(Y=1) \quad \text{[bits/símbolo]}

### 2.4. Ruido del Canal o Entropía Condicional H(Y|X)
Representa la cantidad promedio de información inútil o incertidumbre añadida por las perturbaciones del canal:

H(Y|X) = H(p) = -p \log_2(p) - (1-p) \log_2(1-p) \quad \text{[bits/símbolo]}

Dado que el BSC es un canal uniforme, el ruido H(Y|X) depende únicamente de p y es totalmente independiente de la distribución de entrada P(X).

### 2.5. Información Mutua I(X;Y)
Es la cantidad real de información que la observación de la salida Y proporciona sobre la entrada X:

I(X;Y) = H(Y) - H(Y|X)

### 2.6. Capacidad del Canal (C) y Condición de Maximización
La capacidad C es el máximo valor que puede alcanzar la información mutua al optimizar la distribución de entrada P(X):

C = \max_{P(X)} I(X;Y) = \max_{P(X)} [H(Y) - H(p)] = 1 - H(p) \quad \text{[bits/símbolo]}

* **Condición de Maximización:** Como H(p) es constante para un p dado, I(X;Y) alcanza su máximo cuando la entropía de salida H(Y) es máxima (H(Y) = 1 bit). Esto ocurre **únicamente cuando la fuente de entrada es equiprobable**, es decir:

P(X=0) = P(X=1) = 0.5
### 2.7 Analisis de convergencia del BER (ley de los grandes numeros)
    
    A medida que la magnitud de la trama aumenta (de 100 a 1.000.000 de bits), la frecuencia
    relativa de errores (BER empírico) se estabiliza y converge de forma precisa hacia la
    probabilidad de error teórica 'p' del canal, reduciendo la varianza muestral.

---

## 3. Explicación Detallada del Código

### 3.1. Servidor (`servidor_bsc.py`)
* **`atender_cliente(cliente, direccion)`:** Maneja la sesión TCP con cada cliente en un hilo independiente (`threading`). Para cada bit recibido, genera un valor pseudoaleatorio mediante `random.random()`. Si dicho valor es menor que `P_ERROR`, invierte el bit (`0` \leftrightarrow `1`); de lo contrario, lo transmite intacto.
* **Protocolo de Enmarcado:** Utiliza `struct.pack("!I", longitud)` para enviar un encabezado de 4 bytes con el tamaño exacto del mensaje, evitando problemas de fragmentación TCP.

### 3.2. Cliente (`cliente_bsc.py`)
* **Módulo de Red y Protocolo (`enviar_mensaje`, `recibir_mensaje`, `recibir_exactamente`):** Garantiza la lectura completa de los bytes indicados en el encabezado TCP.
* **Conversión de Formato (`texto_a_binario`, `binario_a_texto`):** Traduce cadenas ASCII a secuencias binarias de 8 bits por carácter y viceversa.
* **Módulo de Cálculo Entrópico (`calcular_entropia_binaria`, `calcular_entropia_general`):** Implementa rigurosamente la fórmula de Shannon - \sum p_i \log_2(p_i), incluyendo protección contra \log_2(0).
* **`ejecutar_fase1(sock)`:**
  - Envía tramas sintéticas de 10^2, 10^4 y 10^6 bits.
  - Compara las tramas recibidas bit a bit y calcula \text{BER} = \frac{\text{errores}}{N}.
  - Transmite el texto `"Teoría de la Información 2026 - Licenciatura en Ciencias de la Computación"` en binario y muestra en consola la degradación por ruido.
* **`ejecutar_fase2(p_estimada, x_binario, y_binario)`:**
  - Construye e imprime la matriz P(Y|X).
  - Calcula las probabilidades de la fuente P(X=0) y P(X=1) del texto transmitido.
  - Evalúa H(Y), H(Y|X), I(X;Y) y la Capacidad C = 1 - H(p).
  - Calcula el porcentaje de capacidad alcanzado (I(X;Y)/C) y emite el análisis de maximización.

---


### Pasos para Ejecutar

1. **Paso 1: Iniciar el Servidor BSC**
   Abra un terminal y ejecute el servidor:
   ```bash
   python3 servidor_bsc.py
   ```
   *El servidor quedará escuchando en el puerto 5555.*

2. **Paso 2: Iniciar el Cliente BSC**
   En una segunda terminal, ejecute el cliente:
   ```bash
   python3 cliente_bsc.py
   ```

---

