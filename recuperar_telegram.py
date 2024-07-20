import pymongo
from telethon import TelegramClient
import hashlib

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


# Lista de canales a recuperar.
#canales = ["xxxxx", "xxxxxx", "xxxxxxx", "xxxxxxx", "xxxxxxx"]
canales = ["xxxxxx", "xxxxxxx"]


# Sustituye estos valores con los datos de tu aplicación.
api_id = 'xxxxxx'
api_hash = 'xxxxxxxx'


# Sustituye estos valores con tu número de teléfono y el nombre de usuario del canal.
phone_number = '+xxxxxxxxx'


# Crear una instancia del cliente
client = TelegramClient('session_name', api_id, api_hash)


#Base de datos donde guaradr los resultados
equipo = "x.x.x.x"
puerto = "27017"


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


async def main():
    await client.start(phone_number)
    print("Conectado a Telegram...")
    for channel_username in canales:
        # Obtener la entidad del canal
        channel = await client.get_entity(channel_username)
        
        # Obtener los mensajes del canal
        async for message in client.iter_messages(channel, limit=100000000000000):  # Obtiene los últimos xxxxxxxx mensajes
            try:
                #print(message.sender_id, message.text)
                #print(message.sender_id)
                print(message.id, channel_username)            
                mensaje = {"_id": message.id, "fecha": message.date, "mensaje": message.text}          
                insertar_mensaje(mensaje, channel_username)
            except Exception as e:
                print(e)
                pass
            
# Ejecutar el cliente
with client:
    client.loop.run_until_complete(main())