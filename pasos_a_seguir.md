# Pasos a Seguir Proyectos 3:

## Fase 1:
### Pico servidor:

- Código Micropython para levantar un punto de acceso en modo servidor. ✅
- Levantar un servidor web. ✅
- Crear página HTML para la configuración del dispositivo. ✅
- Código Micropython para leer el archivo html en tramos de 2048 y enviarlo. [Intentar reducir tiempos]. ✅
- Código Javascript de cifrado de los datos de configuración con AES. (aes-js). ✅
- Código Micropython para el desencriptado de AES. (pyaes). ✅
- Código Micropython para guardar lo desencriptado en un archivo de configuración. (.txt) ✅
- Código Micropython para cambiar de modo Servidor a modo Cliente. (Cambio a Fase 2). ✅

- Arreglar Router.

## Fase 2:
### Pico cliente:

- Código para incorporar los datos del archivo de configuración como variables, lectura del archivo.
- Probar que todo funciona como en proyectos 2.
- Enviar los datos securizados SSL.
- Introducir clave de Autentificación de cara al servidor.
- Paquetización de los datos con el protocolo MQTT.

## Fase 3:
### Servidor Externo:

- Modificar el servidor. Intentar hacer una APP con https://streamlit.io/ 
- Levantar un MQTT Broker, Mosquito es el más famoso.
- Probar si Nodered sirve.

