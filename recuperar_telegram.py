import pymongo
from telethon import TelegramClient

# Lista de los nombres de los canales que deseamos descargar.
canales = ["xxxxxxxxxxxx", "xxxxxxxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxxxxxxxxxxx"]

# Valores para configurar la aplicación del cliente de Telegram.
api_id = 'xxxxxxxxxxxxxxxxxxxxx'
api_hash = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Número de teléfono y nombre de usuario del canal que deseamos conectar a.
phone_number = '+xxxxxxxxxxxxxxxxx'

# Inicializa un cliente de Telegram.
client = TelegramClient('session_name', api_id, api_hash)

# Dirección y puerto donde se encuentra la base de datos MongoDB en el que almacenaremos los mensajes
equipo = "x.x.x.x"
puerto = "27017"

def insertar_mensaje(mensaje, channel_username):
    """
    Esta función recibe un mensaje y el nombre del canal como parámetros.
    Intenta insertar el mensaje en la base de datos MongoDB en una colección llamada "mensajes"
    que se encuentra en una base de datos con el mismo nombre que el canal.
    Si hay un error, imprime la excepción. Cierre la conexión a la base de datos finalmente.
    """
    try:
        client = pymongo.MongoClient(f"mongodb://{equipo}:{puerto}/")
        db = client[channel_username]
        col = db["mensajes"]
        col.insert_one(mensaje)
    except Exception as e:
        print(e)
    finally:
        client.close()


async def main():
    """
    Inicia la conexión con Telegram, imprime que está conectado y luego itera a través de cada canal en nuestra lista.
    Para cada canal, obtiene la entidad del canal usando el método 'get_entity', lo que nos permite interactuar directamente con él.

    A continuación, usa iter_messages para recoger los mensajes del canal. Los parámetros indican que queremos descargar todos los mensajes.
    Luego, imprime la información del mensaje y ejecuta la función 'insertar_mensaje' para almacenarlo en MongoDB.
    """
    await client.start(phone_number)
    print("Conectado a Telegram")

    for channel_username in canales:
        # Obtener la entidad del canal
        channel = await client.get_entity(channel_username)

        async for message in client.iter_messages(channel, limit=10):
            print(message.sender_id, message.text)

            mensaje = {"_id": message.text, "fecha": message.date}

            insertar_mensaje(mensaje, channel_username)

# Finalmente se ejecuta el cliente
with client:
    client.loop.run_until_complete(main())
