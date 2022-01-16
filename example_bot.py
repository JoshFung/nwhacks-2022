import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='>')


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Testing!"))
    print(f'Successfully logged in and booted...!')


@bot.command()
async def test(ctx, *arg):
    await ctx.send('{}'.format(' '.join(arg)))


@bot.command()
async def play(ctx, url : str):
    # saves file called song.mp3 in local directory
    # if it already exists, we'll replace it
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current song to finish")

    # chooses channel based on where user is -- returns error if not in one
    try:
        vc = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
    except AttributeError:
        await ctx.send("You are not in a channel!")
        return

    # connects to channel
    try:
        await vc.connect()
    except discord.ClientException:
        print("Already connected!")

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    # run command
    os.system("spotdl " + url)

    snip_there = os.path.isfile("snip.mp3")
    try:
        if snip_there:
            os.remove("snip.mp3")
    except PermissionError:
        await ctx.send("Wait for the current song to finish")

    # rename song
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")

    # run ffmpeg command to cut snippet and rename, then play
    os.system("ffmpeg -y -ss 00:00:30.0 -i song.mp3 -t 00:00:05.0 -c copy snip.mp3")
    voice.play(discord.FFmpegPCMAudio("snip.mp3"))


@bot.command()
async def disconnect(ctx):
    if ctx.voice_client and ctx.author.voice.channel and ctx.author.voice.channel == \
            ctx.voice_client.channel:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnecting...")
    else:
        await ctx.send("You have to be connected to the same voice channel to disconnect me.")


# token
bot.run('OTMyMDE1NjkxMTY1NDkxMjIx.YeM1QA.80vYLWaj7ulCWK8n8dJWLepkWkU')
