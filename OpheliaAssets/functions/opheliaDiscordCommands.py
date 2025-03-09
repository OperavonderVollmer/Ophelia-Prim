import discord

#target, command_name, command_desc, mode, args
async def sendLongMessage(resp, senderInfo, isTargeted=False):
    if not resp: return
    is_ephemeral = senderInfo["itself"].response.is_done()  # Check if it's ephemeral

    while len(resp) > 2000:
        cutoff = resp[:2000].rfind("\n") 
        if cutoff == -1:  
            cutoff = 2000 
        
        chunk = resp[:cutoff]  
        resp = resp[cutoff:].lstrip() 
        
        if not isTargeted:
            await senderInfo["itself"].followup.send(chunk, ephemeral=is_ephemeral) 
        else: 
            await senderInfo["itself"].followup.send(chunk)
    if resp and len(resp) > 0:
        if not isTargeted:
            await senderInfo["itself"].followup.send(resp, ephemeral=is_ephemeral)
        else:
            await senderInfo["itself"].followup.send(resp)
            
def runPlugin(command_name: str, mode: str = "", args: str = "", act: discord.Interaction = None):
    from opheliaPlugins import plugins
    from functions.opheliaDiscord import discordTokens, sendChannel, discordLoop
    from functions.sanitize import sanitizeText
    from functions.opheliaAsync import async_to_sync_params, async_to_sync
    from opheliaNeurals import opheliaLocal, getRandomDialogue

    senderInfo = {
        "name": act.user.name,
        "id": act.user.id,
        "guild": act.guild,  # will return None if sent from DM
        "voiceClients": discord.utils.get(act.client.voice_clients, guild=act.guild),
        "vcChannel": act.user.voice.channel if act.user.voice else None,
        "discriminator": act.user.discriminator,
        "itself": act
    }

    if opheliaLocal and senderInfo["id"] not in discordTokens["authorizedUsers"]:
        async_to_sync_params(sendLongMessage, discordLoop, "Ophelia is currently in local mode. Please contact `Opera` for assistance.", senderInfo=senderInfo)
        return
    
    comm = command_name.capitalize()
    if plugins[comm].getOperaOnly() and senderInfo["id"] not in discordTokens["authorizedUsers"]:
        return "You are not authorized to use this command"
    
    if mode != "": command = f"{mode} {args}"
    else: command = args    
    # sanitize text, if return is false, immediately delete the user's message 
    if sanitizeText(command) == None: 
        async_to_sync(sendChannel(f"User: {senderInfo['name']} | Channel: {senderInfo['guild']}\nMessage: ```{command}```\nTimestamp: {senderInfo['itself'].created_at}", "warningChannel"), discordLoop)
        async_to_sync_params(sendLongMessage, discordLoop, resp=getRandomDialogue("dirty_messages"), isTargeted=True, senderInfo=senderInfo)
        return
    resp = plugins[comm].cheatResult(command = command, senderInfo = senderInfo)
    if resp == "556036": return "Execution finished successfully"
    print(f"response: {resp}")
    async_to_sync_params(sendLongMessage, discordLoop, resp=resp, senderInfo=senderInfo)
    return  



def setupCommands(tree):
    from opheliaPlugins import plugins
    
    print("Setting up commands...")

    @tree.command(name="sync", description="Manually sync commands")
    async def sync(interaction: discord.Interaction):
        try:
            synced = await tree.sync()
            await interaction.response.send_message(f"Synced {len(synced)} commands successfully!")
        except Exception as e:
            await interaction.response.send_message(f"Sync failed: {e}")

    for key in plugins:
        target = plugins[key]
        command_name = target.getName().lower()
        command_desc = target.getDesc()
        if not target.getNeedsArgs():
            def create_command_callback(command_name):
                async def command_callback(act: discord.Interaction):
                    await act.response.defer(ephemeral=True)
                    runPlugin(command_name=command_name, act=act)
                return command_callback
            tree.command(name=command_name, description=command_desc)(create_command_callback(command_name))

        elif not hasattr(target, "getModes"):
            def create_command_callback(command_name):
                async def command_callback(act: discord.Interaction, args:str = ""):
                    await act.response.defer(ephemeral=True)
                    runPlugin(command_name=command_name, args=args, act=act)
                return command_callback
            tree.command(name=command_name, description=command_desc)(create_command_callback(command_name))

        elif hasattr(target, "getModes"):
            def create_command_callback(command_name):
                async def command_callback(act: discord.Interaction, mode: str, args:str = ""):
                    await act.response.defer(ephemeral=True)
                    runPlugin(command_name=command_name, mode=mode, args=args, act=act)
                return command_callback
            choices = [discord.app_commands.Choice(name=option, value=option) for option in target.getModes()]
            decorated = discord.app_commands.choices(mode=choices)(create_command_callback(command_name))
            tree.command(name=command_name, description=command_desc)(decorated)
                    

    return "Discord command setup completed"
    

    
async def join(interaction: discord.Interaction):
    senderInfo = {
        "name": interaction.user.name,
        "id": interaction.user.id,
        "voiceClients": interaction.client.voice_clients,
        "vcChannel": interaction.user.voice.channel if interaction.user.voice else None,
        "guild": interaction.guild,  # will return None if sent from DM
        "discriminator": interaction.user.discriminator,
        "itself": interaction
    }

    if senderInfo["vcChannel"]:  
        channel = senderInfo["vcChannel"]        
        voice_client = discord.utils.get(senderInfo["voiceClients"], guild=senderInfo["guild"])

        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
            await interaction.response.send_message(f"Moved to {channel.name}")
            return
        try:
            await channel.connect()
            await interaction.response.send_message(f"Joined {channel.name}")
        except Exception as e:
            await interaction.response.send_message(f"Failed to join {channel.name}: {e}")
        return

    else:
        await interaction.response.send_message("You're not in a voice channel!")
    
