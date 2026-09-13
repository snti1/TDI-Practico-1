# 7. Detección de Errores: Códigos de Control (Checksum) El sistema de identificación tributaria en Argentina (CUIT/CUIL) utiliza un dígito verificador para detectar alteraciones o errores de tipeo comunes, basándose en el algoritmo de Módulo 11.

¿Qué hace matemáticamente?

Para un CUIT como:

20-12345678-6

tomamos los primeros 10 dígitos:

2 0 1 2 3 4 5 6 7 8

y los multiplicamos por los pesos:

5 4 3 2 7 6 5 4 3 2

Es decir:

2×5 + 0×4 + 1×3 + 2×2 + 3×7 +
4×6 + 5×5 + 6×4 + 7×3 + 8×2

Luego:

calculamos el modulo 11 de la suma 

suma % 11

y calculamos:

11 - resto

El resultado se transforma según las reglas del algoritmo y se compara con el décimo primer dígito, que es el dígito verificador.

¿Por qué sirve como código de detección de errores?

El CUIT es un código sistemático de detección de errores porque los primeros 10 dígitos contienen la información original y el último se calcula a partir de ellos.

ejecucion:
el usuario debe ingresar su cuit/cuil (11 digitos) y el programa
,mediante el algoritmo de validacion, analizara si el codigo de seguridad ingresado es Valido o Invalido y lo notificara 