import discord
# import logging
#
# logging.basicConfig(level=logging.INFO)

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # ignores its own messages
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('OTMyMDE1NjkxMTY1NDkxMjIx.YeM1QA.80vYLWaj7ulCWK8n8dJWLepkWkU')