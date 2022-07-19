# Problemas encontrados durante la realización del proyecto:

### Encriptación AES de la primera fase:

A la hora de la configuración del dispositivo, cuando el usuario accede a la página de configuración del dispositivo (que se ofrece en modo servidor web) y configura el dispositivo, esa información debe enviarse cifrada al dispositivo, evitando así que un ataque de ManInTheMiddle pueda leer y modificar los datos.
El problema está en que la página web trabaja con javascript y el dispositivo con micropython. El algoritmo de AES es lo suficientemente robusto como para que un ligero cambio en el texto provoque un texto ilegible y lo mismo pasa con un ligero cambio en el algoritmo. La mayoría de los códigos y librerías de ambos lenguajes están diseñados para encryptar y desencriptar con el mismo código (del mismo lenguaje), el problema surje cuando se intentan utilizar 2 lenguajes diferentes. Además si a esto le sumamos la variación de implementaciones de AES (CBC, CTR, CFB, OFB, ECB), las longitudes de claves, las claves son dadas en formatos diferentes y que el término "password" y "key" no es el mismo, auque muchos códigos lo confundan, crean un escenario perfecto para que el texto cifrado mediante un algoritmo de js no cuadre con el descifrado de uno de python, auque cumpla las mismas características mencionadas anteriormente.

Otro de los grandes problemas es que la memoria de la raspberry pico es de 2MB por lo que no caben grandes librerías criptográficas de python. Por lo que hay que buscar librerías especializadas en cifrado AES y esto reduce el numero de implemtaciones, teniendo que rebajarse a lo que marque dicho código, siendo este el punto de cuello de botella más significativo.

Intentos:
- Intentar correr el mismo lenguaje y código tanto en el buscador como en el dispositivo para encriptar y desencriptar (un poco chapuza), para ello he intentado meter una libreria en la pico para corre javascript en python, pero no cabe, es demasiado pesada; y, posteriormente como otra alternativa he intentado correr scripts de python en html (se puede y funciona, pero hay un problema a la hora del formato que no deja la pico enviar la página html si tiene el escript de python).

- Al tener el cuello de botella de que solo unas pocas librerías de python pueden ser incorporadas al microcontrolador por su espacio limitado he empezado a bucar y probar librerías de python antes que las de javaescript. Las librerías de python probadas y que servirían serían:
    - pyaes: está en pypi, y su github es: https://github.com/ricmoo/pyaes, funciona pero no entiendo en que formato está la salida del cifrado y la documentación es bastante mala.
    - maes : esta librería no está en pypi, pero si se descarga uno el código y lo añade manualmente funciona, su página de github es: https://github.com/piaca/micropython-aes, la salida está en un formato entendible.
    - su.aes: no funciona, necesita la librería crypto y es demasiado pesada como para meterla en la pico, su github es: https://github.com/zhaolins/su.aes/blob/master/src/su/aes.py
    - aes-vial y aes-keywrap: tampoco funcionan importan la librería crypto.cipher.
    - aes: funciona, pero su documentación es muy mala, y el código no tienen sentido, así como la salida del cifrado y su formato. Su github es: https://github.com/DonggeunKwon/aes 

- Voy a intentar crear una librería ligera especializada en AES basada en la librería pycryptodome, o también llamada crypto a la que anteriormente me he referido. Esta librería de python está especializada en todo tipo de cifrados, pero es muy pesada para incorporarla en el microcontrolador, concretamente pesa 82,7 MB y el microcontrolador solo tiene espacio para 2MB. Voy a bajarme la librería e ir limpiadola de todo aquello que no necesite para ejecutar AES. Pasos:
1. Descargar el repo de github donde se encuentra: https://github.com/Legrandin/pycryptodome.git
2. Ver el tamaño de la carpeta: </br>
![](Tama%C3%B1oCrypto.png)
3. Realizar un pequeño programa que utilice crypto, como me interesa el programa que se vicula al aes de JS y supuestamente funcuiona utilizaré ese, se encuentra en: https://medium.com/@sachadehe/encrypt-decrypt-data-between-python-3-and-javascript-true-aes-algorithm-7c4e2fa3a9ff
5. Ir eliminando cosas y ejecutanto el código, hasta que algo se rompa.

    -  https://github.com/Legrandin/pycryptodome/blob/master/lib/Crypto/Cipher/AES.py [9.3 KB]

    ```python
    import sys
    from Crypto.Cipher import _create_cipher
    from Crypto.Util._raw_api import (load_pycryptodome_raw_lib,
                                  VoidPointer, SmartPointer,
                                  c_size_t, c_uint8_ptr)
    from Crypto.Util import _cpu_features
    from Crypto.Random import 
    
    - km
    
### Las librerías de JS referenciadas con https://... no funcionan aqui:
Las librerías de Javaescript que son llamadas como importación mediante src=https://... no funcionan en el dispositivo cuando hace de servidor web porque estas librerías necesitan internet. Pero la librería de Javascript para AES es necesaria, para ello he tenido que descargarla entera (62,2 KB - https://github.com/ricmoo/aes-js/blob/master/index.js) e introducirla en un script en la página de configuración html. Esto ocasiona un problema puesto que a la página hay que sumarle los 62,2 KB de código adicional a enviar cuando se solicite la página, y esta solo puede ser enviada en tramos de 2048 Bytes, es decir, 2,048KB, por lo que la página tarda en ser enviada unos 30 segundos, he probado a enviarla más rápido y empieza a haber fallos en el código entregado y ensamblado.

### Problemas con la librería pyaes en desencriptado de la primera fase:
Error con la memoria RAM de la pico, a la hora de importar todos los paquetes necesarios el de pyaes da problemas porque se queda supuestamente sin memoria. Da el siguiente error:

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/lib/pyaes/__init__.py", line 51, in <module>
MemoryError: memory allocation failed, allocating 164 bytes
```

Y no se cual es el problema. La librería pyaes es demasido sensible con la pico. Aunque corra un programa sin casi nada muchas veces da fallo. He encontrado el siguiente manual de buenas prácticas para programar en micropython: https://docs.micropython.org/en/latest/reference/constrained.html#fragmentation. 
No se debe olvidar que se está programando en un dispositivo con una memoria RAM limitada y muchas de las librerías de python no tienen en cuanta esta característica limitante, ya que son diseñadas para correr en ordenadores con suficiente RAM, pyaes es una de ellas.
Es por ello que he cambiado a la librería maes.py que es una librería de AES creada especialmente para micropython.