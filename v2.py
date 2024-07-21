# Import necessary libraries for connection to Telegram API (telethon) and MongoDB (pymongo)
import pymongo
from pymongo import MongoClient
from telethon import TelegramClient
import hashlib

# Initialize a list that will hold the channel usernames from the text file
canales = []

# Read each line of channels from 'lista_canales_telegram.txt' and store it without newline characters
with open('lista_canales_telegram.txt', 'r') as file:
    for line in file:
        line = line.strip("\n")
        canales.append(line.strip())

# Replace 'xxxxx' with your actual values for the API ID, API hash, Telegram phone number and channel username.
api_id = 'xxxxx'
api_hash = 'xxxxxxxx'
phone_number = '+xxxxxxxxx'

# Establish a connection to the Telegram client using the API credentials
client = TelegramClient('session_name', api_id, api_hash)

# Define function to generate an ID from given date or message. Returns None if both are None.
def generar_id(fecha=None, mensaje=None):
    # Implementation for generating IDs based on input parameters

# Define function to count documents in MongoDB collection
async def contar_documentos(coleccion):
    try:
        client = MongoClient('localhost', 27017)  # Establish a connection to the MongoDB server
        db = client['telegram']                  # Selects 'telegram' database
        collection = db[coleccion]              # Selects specific collection within the 'telegram' database

        count = await collection.count_documents({})  # Counts documents in the specified collection
    except Exception as e:
        print(f"Ocurrió un error al interactuar con MongoDB: {e}")
        return None
    
    finally:
        client.close()                          # Closes the connection to MongoDB

# Define function to count messages in a Telegram channel asynchronously using telethon's async loop.
async def contar_mensajes(channel_username):
    await client.start()                      # Start the client session
    channel = await client.get_entity(channel_username)  # Get entity of the specified channel
    
    total_messages = sum(1 for _ in await client.iter_messages(channel))  # Count messages using iterator
    return total_messages

# Define function to insert a message into MongoDB's specific collection.
def insertar_mensaje(mensaje, channel_username):
    try:
        client = MongoClient(f"mongodb://{equipo}:{puerto}/")   # Establish connection with MongoDB server
        db = client['telegram']
        collection = db[channel_username]
        
        # Insert the message document into the specified collection
        collection.insert_one(mensaje)
    
    except Exception as e:
        print(e)
    
    finally:
        client.close()  # Close the MongoDB connection

# Define main function to handle the asynchronous logic for each channel.
async def principal(channel_username, limit):
    await client.start()
    channel = await client.get_entity(channel_username)

    async for message in client.iter_messages(channel, limit=limit):  # Get messages within the specified limit
        try:
            print(message.id, channel_username)              # Print ID and channel username
        
            mensaje = {"_id": message.id, "fecha": message.date, "mensaje": message.text}
            insertar_mensaje(mensaje, channel_username)
        
        except Exception as e:
            print(e)

# Main execution loop for each channel in 'canales' list
with client:
    for channel_username in canales:
        print(channel_username)  
        
        total_mensajes_canal = await contar_mensajes(channel_username)
        print(f'Número total de mensajes en el canal {channel_username}: {total_mensajes_canal}') 
        
        total_documentos = await contar_documentos(channel_username)
        print(f'Número total de documentos en la colección {channel_username}: {total_documentos}')
        
        mensajes_a_recuperar = total_mensajes_canal - total_documentos
        print(f'Número de mensajes a recuperar en el canal {channel_username}: {mensajes_a_recuperar}')
        
        await principal(channel_username, mensajes_a_recuperar)
