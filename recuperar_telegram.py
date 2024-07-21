import pymongo
from pymongo import MongoClient
from telethon import TelegramClient
import hashlib

canales = []

with open('lista_canales_telegram.txt', 'r') as file:
    for line in file:
        line = line.strip("\n")
        canales.append(line.strip())


# Sustituye estos valores con los datos de tu aplicación.
api_id = 'xxxxx'
api_hash = 'xxxxxxxx'


# Sustituye estos valores con tu número de teléfono y el nombre de usuario del canal.
phone_number = '+xxxxxxxxx'


# Crear una instancia del cliente
client = TelegramClient('session_name', api_id, api_hash)


#Base de datos donde guaradr los resultados
equipo = "localhost"
puerto = "27017"

def generar_id(fecha, mensaje):
    if fecha is None:
        id = hashlib.sha512(mensaje.encode()).hexdigest()
    elif mensaje is None:
        id = hashlib.sha512(fecha.encode()).hexdigest()    
    elif mensaje is None and fecha is None:
        id = None        
    else:
        combinacion_entrada = fecha + mensaje
        id = hashlib.sha512(combinacion_entrada.encode()).hexdigest() 
    return id


def contar_documentos(coleccion):
    # Establecer conexión a MongoDB
    client = MongoClient('localhost', 27017)
    
    # Seleccionar la base de datos y la colección
    db = client['telegram']
    collection = db[coleccion]
    
    try:
        # Cuenta los documentos en la coleccion seleccionada
        count = collection.count_documents({})
        
        return count

    except Exception as e:
        print(f"Ocurrió un error al interactuar con MongoDB: {e}")
        return None
    
    finally:
        client.close()  # Cerrar conexión a MongoDB


async def count_messages(channel_username):
    # Conéctate a Telegram
    await client.start()
    
    # Obtén la entidad del canal
    channel = await client.get_entity(channel_username)
    
    # Usa el método get_messages para contar los mensajes
    total_messages = 0
    async for message in client.iter_messages(channel):
        total_messages += 1
    
    return total_messages

def insertar_mensaje(mensaje, channel_username):
    try:
        client = pymongo.MongoClient(f"mongodb://{equipo}:{puerto}/")
        db = client["telegram"]
        col = db[channel_username]
        col.insert_one(mensaje)    
    except Exception as e:
        print(e)
    finally:
        client.close()


async def main(channel_username, limit):
    await client.start(phone_number)
    print("Conectado a Telegram")
    
    # Obtener la entidad del canal
    channel = await client.get_entity(channel_username)
        
    # Obtener los mensajes del canal
    async for message in client.iter_messages(channel, limit):  # Obtiene los últimos xxxxxxxx mensajes
        try:
            #print(message.sender_id, message.text)
            #print(message.sender_id)
            print(message.id, channel_username)            
            mensaje = {"_id": message.id, "fecha": message.date, "mensaje": message.text}          
            insertar_mensaje(mensaje, channel_username)
        except Exception as e:
            print(e)
            pass


with client:
    for channel_username in canales:
        print(channel_username)       
        total_mensajes_canal = client.loop.run_until_complete(count_messages(channel_username))
        print(f'Número total de mensajes en el canal {channel_username}: {total_mensajes_canal}') 
        total_documentos = contar_documentos(channel_username)
        print(f'Número total de documentos en la colección {channel_username}: {total_documentos}')   
        mensajes_a_recuperar = total_mensajes_canal - total_documentos
        print(f'Número de mensajes a recuperar en el canal {channel_username}: {mensajes_a_recuperar}')

        client.loop.run_until_complete(main(channel_username, mensajes_a_recuperar))
'''

El código proporcionado es una mezcla de varias tecnologías y frameworks. Se utiliza la biblioteca pymongo para interactuar con una base de datos MongoDB y la biblioteca Telethon para interactuar con la API de Telegram.

Aquí está un resumen detallado del código:

Importaciones
El código importa las siguientes librerías y módulos:
   1 pymongo: Para la interacción con bases de datos MongoDB.
   2 TelegramClient: De Telethon, que se usa para interactuar con el API de Telegram.
   3 hashlib: Para generar ID basados en mensajes y fechas.

Configuración de Canales
El código lee una lista de canales de Telegram desde un archivo (lista_canales_telegram.txt). Cada canal se añade a la lista canales.

Configuración de Datos de Acceso a Telegram
Los datos de acceso a Telegram, como api_id y api_hash, se reemplazan por las correspondientes en el código.

Creación del Cliente de Telegram
Un cliente de Telegram se crea utilizando los datos de API y número de teléfono proporcionados.

Generar ID
La función generar_id genera un identificador único basado en la fecha y mensaje proporcionados. Utiliza la función hashlib.sha512() para generar el hash del ID.

Contando Documentos en MongoDB
La función contar_documentos cuenta los documentos en una coleccion específica de una base de datos MongoDB utilizando el cliente MongoClient.

Recuento de Mensajes en Telegram
La función count_messages recuenta los mensajes en un canal específico proporcionado como argumento.

Insertando Mensajes a MongoDB
La función insertar_mensaje inserta un mensaje en la coleccion correspondiente de la base de datos MongoDB.

Función Principal main
El bloque async def main(channel_username, limit) es la función principal que se ejecuta para cada canal. Realiza lo siguiente:

   1 Conecta al Telegram.
   2 Obtiene la entidad del canal específico.
   3 Utiliza count_messages para obtener el total de mensajes en el canal.
   4 Compara esto con el número total de documentos existentes en MongoDB para determinar cuántos mensajes faltan recuperar.
   5 Luego ejecuta una tarea asincrónica main(channel_username, mensajes_a_recuperar) para recoger y almacenar los mensajes que aún no se han recuperado.

    Ejecución
El código finalmente itera a través de la lista de canales, realiza todas las operaciones descritas anteriormente para cada canal.


'''