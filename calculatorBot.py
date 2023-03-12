import os
from math import sqrt
from discord import* 
import discord
from dotenv import load_dotenv
import time
from steam import Steam
from decouple import config


load_dotenv()
token = os.getenv("discordToken")
textChannel = os.getenv("discordChannel")
steamKey = os.getenv("steamKey")

intents = discord.Intents.all()
client = discord.Client(intents=intents)
steam = Steam(steamKey)


#print(steam.users.get_owned_games("76561198068524273"))
#print(steam.apps.get_app_details(105600))
#games = steam.users.get_user_recently_played_games("76561198068524273")
#print(steam.users.get_user_friends_list("76561198068524273"))

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
        
        tempString = sentMessage.split(" ")[0]
        
        match tempString:
            
            case "!calculate":
                await math(sentMessage, message)

            case "!steamAssets":
                await steamAssets(sentMessage, message)
                
            case "!steamUser":
                await steamUser(sentMessage, message)

            case "!steamCompare":
                await steamCompare(sentMessage, message)
            
            case "!steamID": 
                await steamID(sentMessage, message)

            case "!info":
                await readInfo(message)

            case "!defeatMyEnemies":
                await defeatMyEnemies(message)

async def steamCompare(sentMessage, message):
    firstLibrary = steam.users.get_owned_games(sentMessage.split(" ")[1])
    secondLibrary = steam.users.get_owned_games(sentMessage.split(" ")[2])
    firstUser = steam.users.get_user_details(sentMessage.split(" ")[1])["player"]["personaname"]
    secondUser = steam.users.get_user_details(sentMessage.split(" ")[2])["player"]["personaname"]
    similarGames = {}
    sameGames = []


    for i in range(firstLibrary["game_count"]):
        similarGames[firstLibrary["games"][i]["name"]] = 1
    
    for j in range(secondLibrary["game_count"]):

        try:
            similarGames[secondLibrary["games"][j]["name"]] += 1
            sameGames.append(secondLibrary["games"][j]["name"])
        except:
            similarGames[secondLibrary["games"][j]["name"]] = 1

    await message.channel.send(firstUser + "'s and " + secondUser + "'s common games: \n" + str(sorted(sameGames)))


async def steamAssets(sentMessage, message):
    steamLibrary = steam.users.get_owned_games(sentMessage.split(" ")[1])
    steamUser = steam.users.get_user_details(sentMessage)["player"]["personaname"]
    value = 0 
    mostExpensiveGame = 0 
    gameCount = steamLibrary["game_count"]
    for i in range(int(gameCount)):
        if i % 100 == 0:
            time.sleep(1) # Prevents discord from pausing the bot due to too much going on.
        currentGame = steamLibrary["games"][i]["name"]
        gameSearched = steam.apps.search_games(currentGame)
        
        if(len(gameSearched["apps"]) > 0):
            gamePrice = gameSearched["apps"][0]["price"]
            if gamePrice.startswith("$"):
                value += float(gamePrice[1:])
                if float(gamePrice[1:]) > mostExpensiveGame:
                    mostExpensiveGame = float(gamePrice[1:])
                    leastCheapGame = currentGame
                    

    await message.channel.send(steamUser + "'s total steam library is worth: $" + str(value) + "\n" + 
                            steamUser + "'s most expensive game is: " + leastCheapGame + " ($" + str(mostExpensiveGame) + ")")
        
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


client.run(token)


