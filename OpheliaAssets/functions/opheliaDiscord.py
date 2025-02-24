import os, asyncio
from dotenv import load_dotenv
from discord import Intents, Client, Message
import discord
from functions import opheliaObey
from functions.sanitize import sanitizeText
import opheliaDialogue as opheDia
import random
import yt_dlp

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
discordLoop = asyncio.get_event_loop()
isOnline = False

async def riposteMessage(message, input):
    powerdown = False
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

async def sendChannel(output, selectedChannel):
    try:
        if not isOnline: return
        channelId = discordTokens[selectedChannel]
        channel = client.get_channel(channelId)
        if channel is not None: await channel.send(output)
        else: print("Channel not found")
    except Exception as e: print(e)

voice_client = None

async def join_voice_channel(channel_id):
    global voice_client
    """Joins a Discord voice channel if not already connected."""
    if voice_client and voice_client.is_connected():
        return voice_client  # Already connected
    
    guild = client.get_guild(discordTokens["guildID"])
    if not guild:
        print("Guild not found")
        return

    voice_channel = guild.get_channel(channel_id)
    if voice_channel and isinstance(voice_channel, discord.VoiceChannel):
        voice_client = await voice_channel.connect()
        return voice_client
    else:
        return None

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
#ffmpeg_opts = {'options': '-vn'}
ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -ac 2 -ar 48000 -b:a 256k -bufsize 512k'
}
async def startMusicStream(song):
    voice_client = await join_voice_channel(discordTokens["voiceChannel"])
    #url = song["url"]
    url = song
    try:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        sound = data["url"]
        player = discord.FFmpegPCMAudio(sound, **ffmpeg_opts)
        voice_client.play(player)
    except Exception as e:
        print(e)

async def pauseMusicStream():
    voice_client = await join_voice_channel(discordTokens["voiceChannel"])
    if voice_client:
        if voice_client.is_paused():
            voice_client.resume()
        else:
            voice_client.pause()
        
    return f"Paused: {voice_client.is_paused()} | Playing: {voice_client.is_playing()}"

@client.event
async def on_ready():
    print("Ophelia is now online on Discord!!")
    global isOnline
    isOnline = True
    
@client.event
async def on_message(message):
    if not isOnline: return
    if message.author == client.user: return
    username = str(message.author)
    messageContent = str(message.content)
    channel = str(message.channel)
    #print(f"{username} said: '{messageContent}' ({channel})")
    await riposteMessage(message, messageContent)

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