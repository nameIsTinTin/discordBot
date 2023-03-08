import os
from discord import* 
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("discordToken")

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# def add(sentMessage):
#     print(sentMessage)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client).split("#")[0])
    

@client.event
async def on_message(message):
    
    sentMessage = message.content
    
    if message.author == client.user: # Halting point after a message 
        return
    
    
    elif sentMessage.startswith('!'): # this makes it so that the message has to start with ! for it to respond
        await message.channel.send("I am {0.user}".format(client).split("#")[0])
        
        tempString = sentMessage[0:4]
        print(tempString)
        
        match tempString:
            
            case "!add":
                await mathAdd(sentMessage, message)
                

async def mathAdd(sentMessage, message):
    value = 0 
    sentMessage = sentMessage[5:]
    for i in sentMessage.split(" "):
        try:
            value += float(i)
        except:
            await message.channel.send("You seem to have a non-number inside of your command")
    
        
    await message.channel.send(str(value))
 

client.run(token)

