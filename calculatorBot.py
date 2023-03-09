import os
from discord import* 
import discord
from dotenv import load_dotenv

from steam import Steam
from decouple import config




load_dotenv()
token = os.getenv("discordToken")
textChannel = os.getenv("discordChannel")
steamKey = os.getenv("steamKey")

intents = discord.Intents.all()
client = discord.Client(intents=intents)
steam = Steam(steamKey)


print(steam.users.get_user_details("76561198068524273"))
games = steam.users.get_user_recently_played_games("76561198068524273")
print(games["total_count"])
print(games["games"][0]["name"])



@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client).split("#")[0])
    await client.get_channel(int(textChannel)).send(open("help.txt","r+").read())
    

@client.event
async def on_message(message):
    
    sentMessage = message.content
    
    if message.author == client.user: # Halting point after a message 
        return
    
    elif sentMessage.startswith('!'): # this makes it so that the message has to start with ! for it to respond
        
        #await message.channel.send("I am {0.user}".format(client).split("#")[0] + ". !info for what I can do.")
        
        tempString = sentMessage.split(" ")[0]
        
        match tempString:
            
            case "!calculate":
                await math(sentMessage, message)

            case "!steamUser":
                await steamUser(sentMessage, message)
            
            case "!steamID": 
                await steamID(sentMessage, message)

            # case "!add":
            #     await mathAdd(sentMessage, message)

            # case "!multiply":
            #     await mathMultiply(sentMessage, message)

            # case "!divide":
            #     await mathDivide(sentMessage, message)

            # case "!minus": 
            #     await mathMinus(sentMessage, message)

            case "!info":
                await readInfo(message)

            case "!defeatMyEnemies":
                await defeatMyEnemies(message)

async def findUserRecentGames(steamGames):
    steamRecentGames = ""
    for i in range(int(steamGames["total_count"])):
              currentGame = steamGames["games"][i]
              gameName = currentGame["name"] 
              gameDetails = steam.apps.search_games(gameName)["apps"][0]
              print(gameName, gameDetails)

              play2Week = int(currentGame["playtime_2weeks"]) // 60
              playForever = int(currentGame["playtime_forever"]) // 60

              gamePrice = gameDetails["price"]
              gameLink = gameDetails["link"]

              steamRecentGames += (f'Game Name: {gameName}\nPlaytime over 2 weeks: {play2Week}\nTotal playtime:  {playForever}\nGame Price: {gamePrice}\nGame URL: {gameLink}\n\n')

    return steamRecentGames 

async def steamID(sentMessage, message):

    try:
        id = sentMessage.split(" ")[1]
        steamUser = steam.users.get_user_details(id)["player"]["personaname"]
        steamID= id
        steamURL = steam.users.get_user_details(id)["player"]["profileurl"]
        steamLevel = steam.users.get_user_steam_level(steamID)["player_level"]
        steamGames = steam.users.get_user_recently_played_games(steamID)
        await message.channel.send(f'Steam User: {steamUser}\n Steam ID: {steamID}\n Steam URL: {steamURL}\n Steam Level: {steamLevel}\n\n')
        await message.channel.send(await findUserRecentGames(steamGames))
        
    except:
        await message.channel.send("Steam ID does not exist or perhaps misspelt.")


async def steamUser(sentMessage, message):

    try:
        name = sentMessage.split(" ")[1]
        steamUser = steam.users.search_user(name)["player"]["personaname"]
        steamID= steam.users.search_user(name)["player"]["steamid"]
        steamURL = steam.users.search_user(name)["player"]["profileurl"]
        steamLevel = steam.users.get_user_steam_level(steamID)
        steamGames = steam.users.get_user_recently_played_games(steamID)
        await message.channel.send(f'Steam User: {steamUser}\n Steam ID: {steamID}\n Steam URL: {steamURL}\n Steam Level: {steamLevel}\n\n')
        await message.channel.send(await findUserRecentGames(steamGames))
        
    except:
        await message.channel.send("Steam user does not exist or perhaps misspelt. Often, profiles are not visible for scanning too so you can try steam ID.")
    

async def math(sentMessage, message):
    try:
        await message.channel.send(eval(sentMessage[10:]))
    except:
        await message.channel.send()

async def defeatMyEnemies(message):
    await message.channel.send(file=discord.File('giphy.gif'))

async def readInfo(message):
    file1 = open("help.txt","r+")
    await message.channel.send(file1.read())


# async def mathMinus(sentMessage, message):
    
#     value = float(sentMessage.split(" ")[1])
#     if len(sentMessage.split(" ")) > 1:
#         for i in sentMessage.split(" ")[2:]:
#             try:
#                 value -= float(i)
#             except:
#                if float(i) == 0.0:
#                 await message.channel.send("ERROR ERROR ERROR")
#                 return
#                elif i != "-" and i != "":
#                 await message.channel.send("You seem to have an invalid value or an incorrect syntax inside of your command : " + str(i) + "\n" + 
#                                                 "Valid values have spaces in between characters such as !minus 1 1 1")
    
        
#     await message.channel.send(str(value))

# async def mathDivide(sentMessage, message):
    
#     value = float(sentMessage.split(" ")[1])
#     #print(value)
#     if len(sentMessage.split(" ")) > 1:
#         for i in sentMessage.split(" ")[2:]:
#             try:
#                 value /= float(i)
#             except:
#                if i != "/" and i != "":
#                 await message.channel.send("You seem to have an invalid value or an incorrect syntax inside of your command : " + str(i) + "\n" + 
#                                                 "Valid values have spaces in between characters such as !divide 1 1 1")
    
        
#     await message.channel.send(str(value))

# async def mathMultiply(sentMessage, message):
#     value = 1
    
#     for i in sentMessage.split(" ")[1:]:
#         try:
#             value *= float(i)
#         except:
#             if len(sentMessage.split(" ")) == 1:
#                 await message.channel.send("Please ensure you have spaces in between your values")
#             elif i != "*" and i != "":
#                 await message.channel.send("You seem to have an invalid value or an incorrect syntax inside of your command : " + str(i) + "\n" + 
#                                            "Valid values have spaces in between characters such as !multiply 1 1 1")
    
        
#     await message.channel.send(str(value))



# async def mathAdd(sentMessage, message):
#     value = 0 
#     sentMessage = sentMessage[5:]
#     for i in sentMessage.split(" "):
#         try:
#             value += float(i)
#         except:
#             if len(sentMessage.split(" ")) == 1:
#                 await message.channel.send("Please ensure you have spaces in between your values")
#             elif i != "+" and i != "":
#                 await message.channel.send("You seem to have an invalid value or an incorrect syntax inside of your command : " + str(i) + "\n" + 
#                                            "Valid values have spaces in between characters such as !add 1 1 1")
    
        
#     await message.channel.send(str(value))
 

client.run(token)


