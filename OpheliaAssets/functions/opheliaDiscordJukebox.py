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
    from functions.opheliaDiscord import join_voice_channel, discordLoop
    voice_client = await join_voice_channel(kwargs["senderInfo"]["vcChannel"])
    url = kwargs["song"]
    if voice_client.is_playing(): voice_client.stop()
    try:
        data = await discordLoop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        sound = data["url"]
        player = discord.FFmpegPCMAudio(sound, **ffmpeg_opts)
        voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(handleSongEnd(), discordLoop))
        return [True, "Now playing: " + data["title"]]
    except Exception as e:
        return [False, e]

async def handleSongEnd(song):
    from functions.opheliaDiscord import sendChannel
    await sendChannel(f"{song} has finished playing", "musicChannel")
    pass

async def pauseMusicStream():
    from functions.opheliaDiscord import join_voice_channel, discordTokens
    voice_client = await join_voice_channel(discordTokens["voiceChannel"])
    if voice_client:
        if voice_client.is_paused():
            voice_client.resume()
        else:
            voice_client.pause()        
    return f"Paused: {voice_client.is_paused()} | Playing: {voice_client.is_playing()}"

async def stopMusicStream():
    from functions.opheliaDiscord import join_voice_channel, discordTokens
    voice_client = await join_voice_channel(discordTokens["voiceChannel"])
    if voice_client:
        voice_client.stop()
    return f"Stopped: {voice_client.is_playing()}"

async def skipMusicStream():
    raise NotImplementedError
    pass