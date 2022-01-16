import discord
from discord.ext import commands
import youtube_dl
import os
# import logging
#
# logging.basicConfig(level=logging.INFO)

# client = discord.Client()
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

    # connects based on user's channel -- returns error if not in one
    try:
        vc = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
    except AttributeError:
        await ctx.send("You are not in a channel!")
        return

    await vc.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    # specifying options for our song download
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    # download video
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


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
