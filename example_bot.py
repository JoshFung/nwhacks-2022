import discord
from discord.ext import commands
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
    # connects based on user's channel -- returns error if not in one
    try:
        vc = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
    except AttributeError:
        await ctx.send("You are not in a channel!")
        return

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice.is_connect():
        await vc.connect()


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
