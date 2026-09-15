# Control de Errores en Códigos Pesados: Algoritmo de Verificación CUIL / CUIT (Módulo 11)

## 1. Descripción del Problema y Enunciado

El objetivo del ejercicio es desarrollar una aplicación en Python que implemente la **verificación, cálculo y validación de integridad** del **CUIL / CUIT** (Código Único de Identificación Laboral / Tributaria en Argentina) mediante la técnica de **códigos pesados (weighted codes)** en base **módulo 11**.

Los códigos pesados son mecanismos no binarios orientados a la detección de errores tipográficos humanos (como la alteración individual de un dígito o el intercambio de posición entre dígitos adyacentes).

### Requerimientos del Enunciado:
1. **Ingreso y Formateo de Datos:**
   * Solicitar la carga de un número de CUIL/CUIT de 11 dígitos sin guiones ni espacios (ej: 20123456784)  para generar el dígito verificador.
2. **Cálculo de la Suma Ponderada (Módulo 11):**
   * Multiplicar cada uno de los primeros 10 dígitos de la secuencia por la serie fija de pesos asignados a cada posición geográfica: [5, 4, 3, 2, 7, 6, 5, 4, 3, 2].
3. **Validación del Dígito Verificador :**
   * Obtener el resto de la suma ponderada módulo 11 y determinar el dígito de control esperado C = 11 - (Suma\mod{11}).
   * Verificar la coincidencia estricta entre el dígito ingresado y el dígito calculado.
4. **Simulación y Prueba de Control de Errores:**
   * Demostrar computacionalmente que el código es capaz de detectar:
     * **Errores de sustitución simple:** Alteración accidental de 1 dígito cualquiera.
     * **Errores de transposición adyacente:** Intercambio no intencionado entre dos dígitos contiguos.

---

## 2. Fundamentos Matemáticos y Teoremas Aplicados

La resolución se fundamenta en la teoría de **códigos detectores de error con ponderación posicional**:

### A. Concepto de Código Pesado (Weighted Code)
Un código pesado asigna una ponderación o "peso" w_i a cada posición i dentro de la palabra de información. A diferencia de un bit de paridad simple (donde todos los pesos son 1), el peso geométrico w_i permite que la posición del error influya directamente en el chequeador de paridad.

### B. Vector de Pesos y Aritmética Modular Módulo 11
Para la secuencia de entrada de 10 dígitos X = [x_1, x_2, x_3, x_4, x_5, x_6, x_7, x_8, x_9, x_{10}], la norma oficial AFIP/ANSES utiliza el siguiente vector de pesos:
W = [w_1, w_2, w_3, w_4, w_5, w_6, w_7, w_8, w_9, w_{10}] = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

### C. Ecuación de la Suma Ponderada
La suma escalar de los productos dígito-peso se calcula como:
S = \sum_{i=1}^{10} x_i \cdot w_i = 5x_1 + 4x_2 + 3x_3 + 2x_4 + 7x_5 + 6x_6 + 5x_7 + 4x_8 + 3x_9 + 2x_{10}

### D. Cálculo del Dígito Verificador (x_{11})
se calcula el resto= suma%11 y luego el digito verificador se obtiene, digito= 11-resto
debido a que el codifo verificador debe ser estrictamente de un solo digito, se encuetran contemplados los casos digito==11 y digito==10, modificandolos por digito =0 y digito=9 respectivamente

### E. Distancia de Hamming y Capacidad de Detección de Errores
* **Distancia Mínima (d_{min}):** El código posee una distancia de Hamming d_{min} = 2.
* **Errores de Sustitución:** Al ser 11 un número primo, para cualquier alteración , la diferencia en la suma multiplicada por el peso correspondiente nunca será múltiplo de 11, garantizando la **detección del 100% de errores simples**.
* **Errores de Transposición:** Al intercambiar posiciones adyacentes, gracias a los pesos correspondientes a los indices, el codigo verificador no coincidira con el ingresado, por lo que se detectan todos los errores de transposición de dígitos vecinos.

---

## 3. Explicación Detallada de las Funciones del Código

A continuación se detalla la arquitectura interna del script `cuil_detector.py`:

### 1. `calcular_digito_verificador(cuil_base)`
* **Propósito:** Calcula el dígito verificador x_{11} para una cadena base de 10 dígitos (prefijo de 2 dígitos + DNI de 8 dígitos).
* **Mecanismo:**
  * Define la lista de pesos `pesos = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]`.
  * Realiza la suma de productos mediante una expresión generadora
  * Calcula el resto R = suma %11
  * Aplica las reglas condicionales para retornar 0 si digito=11 o 9 si digito=10



### 2. Bloque Principal (`if __name__ == "__main__":`)
* recibe el cuil, analiza si el nro ingresado, tiene 11 digitos
* llama a la funcion calcular_digito_verificador
*   compara el digito verificador con el ingresado
*  imprime en consola los resultados de la simulación de errores.

---

