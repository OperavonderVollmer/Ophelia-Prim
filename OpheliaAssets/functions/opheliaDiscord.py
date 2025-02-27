import os, asyncio
from dotenv import load_dotenv
from discord import Intents, Client, Message
import discord
from discord.ext import commands
from functions import opheliaObey
from functions.sanitize import sanitizeText
import opheliaDialogue as opheDia
import random
import yt_dlp
import datetime
from functions.opheliaDiscordCommands import setupCommands

load_dotenv()
discordTokens = {
    "discordToken": str(os.getenv("discordToken")),
    "logChannel": int(os.getenv("logChannel")),
    "deepLogChannel": int(os.getenv("deepLogChannel")),
    "warningChannel": int(os.getenv("warningChannel")),
    "musicChannel": int(os.getenv("musicChannel")),
    "voiceChannel": int(os.getenv("voiceChannel")),
    "guildID": int(os.getenv("guildId")),
    "authorizedUsers": list(map(int, os.getenv("authorizedUsers", "").split(",")))
}
intents = Intents.default()
intents.message_content = True #NOQA
client = Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
discordLoop = asyncio.get_event_loop()
isOnline = False

@client.event
async def on_ready():
    print(setupCommands(tree))
    global isOnline
    isOnline = True
    """try:
        synced = await tree.sync()  # Attempt to sync commands
        print(f"Synced {len(synced)} commands successfully!")
    except Exception as e:
        print(f"Failed to sync commands: {e}")"""
    print("Ophelia is now online on Discord!!")
    
@client.event
async def on_message(message):
    if not isOnline: return
    if message.author == client.user: return
    await riposteMessage(message)

def wakeOpheliaDiscord():
    print("Starting Ophelia on Discord...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(discordLoop)
    loop.create_task(client.start(discordTokens["discordToken"]))
    return loop

async def stopOpheliaDiscord():
    global isOnline
    isOnline = False
    await client.close()


async def riposteMessage(message):
    input = message.content
    if not input: print("User message is empty. Probably an intents issue, try to get enable intents")
    if sanitizeText(input) is None: 
        await sendChannel(f"User: {message.author} | Channel: {message.channel}\nMessage: ```{message.content}```\nTimestamp: {message.created_at}", "warningChannel")
        output = random.choice(opheDia.dialogue["dirty_messages"])
    else: 
        if isLoud := input[0] == "!": input = input[1:]

        if "operate" in input and message.author.id not in discordTokens["authorizedUsers"]: output = "User is not authorized to make operate commands"
        else:
            output = opheliaObey.opheliaDo(input, speechSource=False, isLoud=isLoud)
            if not output: output = f"Please format your command properly. ```command <command> <mode if any> <args if any>.``` Add a ! in front of your command to activate TTS."
            if output == "556036": output = "Command was executed"
    try: 
        print(f"Sending message `{output}`")
        if isPrivate :=  input[0] == "?" : input = input[1:] 
        if isPrivate:
            await message.author.send(output)
        else:
            await message.channel.send(output)
    except Exception as e: print(e)

async def sendMessage(output, destination):

    pass

async def sendChannel(output, selectedChannel):
    try:
        if not isOnline: return
        channelId = discordTokens[selectedChannel]
        channel = client.get_channel(channelId)
        if channel is not None: await channel.send(output)
        else: print("Channel not found")
    except Exception as e: print(e)

async def join_voice_channel(**kwargs):
    senderInfo = kwargs["senderInfo"]
    channel = senderInfo["vcChannel"]
    voiceClient = discord.utils.get(client.voice_clients, guild=senderInfo["guild"])
    print(f"VOICE CLIENT = {voiceClient}")
    if voiceClient and voiceClient.is_connected():
        if voiceClient.channel == channel: 
            print("ITS THE SAME VOICE CLIENT")
            return voiceClient 
        print("""ITS NOT THE SAME VOICE CLIENT""")
        await voiceClient.move_to(channel)
        return voiceClient    
    print("BOT NOT IN VOICE CHANNEL")
    return await channel.connect()


async def leaveVoiceChannel():

    voice_client = await join_voice_channel(discordTokens["voiceChannel"])
    if voice_client:
        await voice_client.disconnect()