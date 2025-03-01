import yt_dlp
import asyncio
import discord

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
#ffmpeg_opts = {'options': '-vn'}
ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -ac 2 -ar 48000 -b:a 256k -bufsize 512k'
}

"""senderInfo = {
        "name": act.user.name,
        "id": act.user.id,
        "voiceClients": act.client.voice_clients,
        "vcChannel": act.user.voice.channel if act.user.voice else None,
        "guild": act.guild,  # will return None if sent from DM
        "discriminator": act.user.discriminator,
        "itself": act
    }"""


# "song": url to song
# "senderInfo": sender info
async def startMusicStream(**kwargs):
    print("AWOOOOOOOOOOOOOOOOOOOOO")
    from functions.opheliaDiscord import join_voice_channel, discordLoop, sendChannel
    senderInfo = kwargs.get("senderInfo", None)
    print("GETTING VOICE CLIENT")
    voice_client = await join_voice_channel(senderInfo = senderInfo)
    print(f"Voice Client: {voice_client}")
    url = kwargs["song"]
    if voice_client.is_playing(): voice_client.stop()
    try:
        data = await discordLoop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        sound = data["url"]
        player = discord.FFmpegPCMAudio(sound, **ffmpeg_opts)
        voice_client.play(player, after=lambda e: handleSongEnd(senderInfo = senderInfo))        
        output = f"{kwargs['outputMessage']} | User: {senderInfo['name']} | User ID: {senderInfo['id']} | Server: {senderInfo['guild']} | Server ID: {senderInfo['guild'].id}"
        await sendChannel(output, "musicChannel")
    except Exception as e:
        print(e)

def handleSongEnd(senderInfo):
    from functions.opheliaDiscord import sendChannel
    from opheliaPlugins import plugins
    import threading, time
    print("handleSongEnd -> Triggering nextSong() asynchronously")
    def nextSong():
        plugins["Jukebox"].nextSong(senderInfo = senderInfo, end=True)
        print("OWARIDA OWARIDA OWARIDA IM GOING BRAZY AAAAAAAAAAAAAAAAA")
    s = threading.Thread(target=nextSong)
    s.start()
    print("handleSongEnd -> Exiting function (nextSong() is running in the background)")
    return

async def pauseMusicStream(**kwargs):
    from functions.opheliaDiscord import join_voice_channel, sendChannel
    senderInfo = kwargs["senderInfo"]
    voice_client = await join_voice_channel(senderInfo = senderInfo)
    if voice_client:
        if voice_client.is_paused():
            voice_client.resume()
        else:
            voice_client.pause()        
    output = f"Paused: {voice_client.is_paused()} | User: {senderInfo['name']} | User ID: {senderInfo['id']} | Server: {senderInfo['guild']} | Server ID: {senderInfo['guild'].id}"
    await sendChannel(output, "musicChannel")
    return
async def stopMusicStream(**kwargs):
    from functions.opheliaDiscord import join_voice_channel, sendChannel
    senderInfo = kwargs["senderInfo"]
    voice_client = await join_voice_channel(senderInfo = senderInfo)
    if voice_client:
        voice_client.stop()
    output = f"Playing: {voice_client.is_playing()} | User: {senderInfo['name']} | User ID: {senderInfo['id']} | Server: {senderInfo['guild']} | Server ID: {senderInfo['guild'].id}"
    await sendChannel(output, "musicChannel")

