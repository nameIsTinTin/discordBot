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
        await message.channel.send("I am {0.user}".format(client).split("#")[0] + ". !info for what I can do.")
        
        tempString = sentMessage.split(" ")[0]
        
        match tempString:
            
            case "!add":
                await mathAdd(sentMessage, message)

            case "!multiply":
                await mathMultiply(sentMessage, message)

            case "!divide":
                await mathDivide(sentMessage, message)

            case "!minus": 
                await mathMinus(sentMessage, message)

            case "!info":
                await readInfo(sentMessage, message)

async def readInfo(sentMessage, message):
    file1 = open("help.txt","r+")
    await message.channel.send(file1.read())


async def mathMinus(sentMessage, message):
    
    value = float(sentMessage.split(" ")[1])
    if len(sentMessage.split(" ")) > 1:
        for i in sentMessage.split(" ")[2:]:
            try:
                value -= float(i)
            except:
               if float(i) == 0.0:
                await message.channel.send("ERROR ERROR ERROR")
                return
               elif i != "-" and i != "":
                await message.channel.send("You seem to have an invalid value or an incorrect syntax inside of your command : " + str(i) + "\n" + 
                                                "Valid values have spaces in between characters such as !minus 1 1 1")
    
        
    await message.channel.send(str(value))

async def mathDivide(sentMessage, message):
    
    value = float(sentMessage.split(" ")[1])
    #print(value)
    if len(sentMessage.split(" ")) > 1:
        for i in sentMessage.split(" ")[2:]:
            try:
                value /= float(i)
            except:
               if i != "/" and i != "":
                await message.channel.send("You seem to have an invalid value or an incorrect syntax inside of your command : " + str(i) + "\n" + 
                                                "Valid values have spaces in between characters such as !divide 1 1 1")
    
        
    await message.channel.send(str(value))

async def mathMultiply(sentMessage, message):
    value = 1
    
    for i in sentMessage.split(" ")[1:]:
        try:
            value *= float(i)
        except:
            if len(sentMessage.split(" ")) == 1:
                await message.channel.send("Please ensure you have spaces in between your values")
            elif i != "*" and i != "":
                await message.channel.send("You seem to have an invalid value or an incorrect syntax inside of your command : " + str(i) + "\n" + 
                                           "Valid values have spaces in between characters such as !multiply 1 1 1")
    
        
    await message.channel.send(str(value))



async def mathAdd(sentMessage, message):
    value = 0 
    sentMessage = sentMessage[5:]
    for i in sentMessage.split(" "):
        try:
            value += float(i)
        except:
            if len(sentMessage.split(" ")) == 1:
                await message.channel.send("Please ensure you have spaces in between your values")
            elif i != "+" and i != "":
                await message.channel.send("You seem to have an invalid value or an incorrect syntax inside of your command : " + str(i) + "\n" + 
                                           "Valid values have spaces in between characters such as !add 1 1 1")
    
        
    await message.channel.send(str(value))
 

client.run(token)

