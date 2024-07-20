import pymongo
from telethon import TelegramClient
import hashlib

"""
Este script está diseñado para recuperar mensajes de canales específicos de Telegram y almacenarlos en una base de datos MongoDB.
Utiliza la biblioteca Telethon para interactuar con la API de Telegram y pymongo para conectarse a MongoDB.
El script genera un ID único para cada mensaje utilizando una combinación de la fecha del mensaje y su contenido,
luego almacena los datos del mensaje en la base de datos.
"""

def generar_id(fecha, mensaje):
    """
    Genera un ID único utilizando el hash SHA512 de la fecha y el contenido del mensaje.
    Si la fecha o el mensaje es None, utiliza el parámetro disponible para el hash.
    """
    if fecha is None:
        id = hashlib.sha512(mensaje.encode()).hexdigest()
    elif mensaje is None:
        id = hashlib.sha512(fecha.encode()).hexdigest()    
    else:
        combinacion_entrada = fecha + mensaje
        id = hashlib.sha512(combinacion_entrada.encode()).hexdigest() 
    return id

# Lista de canales de los que se recuperarán mensajes
canales = ["xxxx", "xxxxx", "xxxxxx", "xxxxxx", "xxxxxxx"]
#canales = ["xxxxxx", "xxxxxxxx"]

# Credenciales de la API de Telegram (reemplazar con las propias)
api_id = 'xxxxxx'
api_hash = 'xxxxxxxxxxxxxxxxxxxxxx'

# Número de teléfono de tu cuenta de Telegram
phone_number = '+xxxxxxxxxxxxxxxxxxxxxxxx'

# Crear una instancia del cliente de Telegram
client = TelegramClient('session_name', api_id, api_hash)

# Detalles de conexión a MongoDB
equipo = "x.x.x.x"
puerto = "27017"

def insertar_mensaje(mensaje, channel_username):
    """
    Inserta un mensaje en la base de datos MongoDB.
    Cada canal tiene su propia base de datos, con una colección 'mensajes'.
    """
    try:
        # Establecer conexión con MongoDB
        client = pymongo.MongoClient(f"mongodb://{equipo}:{puerto}/")
        db = client[channel_username]
        col = db["mensajes"]
        # Insertar el mensaje en la base de datos
        col.insert_one(mensaje)    
    except Exception as e:
        print(e)
    finally:
        # Asegurar que la conexión a la base de datos se cierre
        client.close()

async def main():
    # Iniciar el cliente de Telegram
    await client.start(phone_number)
    print("Conectado a Telegram")
    
    for channel_username in canales:
        # Obtener la entidad del canal
        channel = await client.get_entity(channel_username)
        
        # Iterar a través de los mensajes en el canal
        async for message in client.iter_messages(channel, limit=100000000000000):  # Recupera hasta 100000000000000 mensajes
            print(message.sender_id, message.text)
            
            # Generar un ID único para el mensaje
            id = generar_id(str(message.date), message.text)
            
            # Preparar los datos del mensaje para la inserción en la base de datos
            mensaje = {"_id": id, "fecha": message.date, "mensaje": message.text}
            
            # Insertar el mensaje en la base de datos
            insertar_mensaje(mensaje, channel_username)

# Ejecutar el cliente
with client:
    client.loop.run_until_complete(main())
