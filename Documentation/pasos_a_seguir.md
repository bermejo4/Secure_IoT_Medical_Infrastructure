# Pasos a Seguir Proyectos 3:

## Fase 1:
### Pico servidor:

- Código Micropython para levantar un punto de acceso (AP) con el dispositivo. ✅
- Configuración del punto de acceso. ✅
- Levantar un servidor web. ✅
- Crear página HTML y JS para la configuración del dispositivo. ✅
- Que la propia pagina web utilice el buscador para cifrar mediante AES.  ✅
- Código Micropython para leer el archivo html en tramos de 2048 y enviarlo. [Intentar reducir tiempos]. ✅
- Código Javascript de cifrado de los datos de configuración con AES. (aes-js). ✅
- Código Micropython para el desencriptado de AES. (maes). ✅
- Código Micropython para guardar lo desencriptado en un archivo de configuración. (.txt). Guardado en formato JSON para mejor lectura posterior. ✅
- Código Micropython para cambiar de modo Servidor a modo Cliente. (Cambio a Fase 2). ✅

- Arreglar Router.✅

## Fase 2:
### Pico cliente:

- Código para incorporar los datos del archivo de configuración como variables, lectura del archivo.  ✅
- Probar que todo funciona como en proyectos 2.  ✅
- Código micropython para cambiar con el interruptor entre modo configuración y modo trabajo (conf_mode and work_mode). ✅
- Para work_mode, código micropython de lectura del archivo de configuración y guardado en variables. ✅
- Enviar los datos securizados SSL. ❌ No va a ser posible. Utilizar la librería de AES. Nuevas Claves. ✅
- Introducir clave de Autentificación de cara al servidor. Las claves de AES serviran como autentificación. ✅
- Paquetización de los datos con el protocolo MQTT.❌ No es posible, los comandos AT necesarios no son soportados por la tarjeta ESP8266. MQTT para servidor.

## Fase 3:
### Servidor Externo:
- Seguir trabajando con el servidor en python, nueva temperatura a incoroporar como variable (temp_mpu).
- El servidor deberá incorporar desencriptado de AES. ✅
- Ver si los tiempos empeoran mucho por el descifrado.
- Archivo de configuración con claves dependiendo de dispositivos. Así se hará la autentificación.
- Por el momento prescindir de código para plotear gráficos.
- Levantar el código del servidor en un docker y probar que funcione.
- Investigar EMQX como posible mqtt broker.
- Levantar EMQX como servicio en docker y comunicar aplicaciones.
- Dejar un puerto abierto desde el exterior para que se pueda solicitar datos del MQTT broker.
- Levantar Node Red en docker. ✅
- Ver que se pueden obtener datos del broker mediante MQTT plugins de Node Red.
- PASAR A LA FASE 4 Y LUEGO VOLVER AQUI CUANDO ESTÉ TODO ACABADO. (INCLUSO EL PAPER !!!)
- ###########################################################################
- Escribir código de pyhton para guardar los datos en una base de datos (MongoDB o Mysql).
- Levantar MongoDB o Mysql en Docker y comunicar con el python server.
- Hacer un dashboard con Streamlit (https://streamlit.io/) a partir de la lectura de la base de datos. (graficado de los datos)
- Levantar streamlit con docker y comunicarlo con la base de datos.
- El Dashboard contará con una opción de lectura de histórico.

## Fase 4: 
### Hardware:
- Incorporar el interruptor para establecer el modo en el que funcionará el aparato. Modo configuración o modo ya Configurado.
- Medir cuanto es el consumo del aparato con el encriptado.