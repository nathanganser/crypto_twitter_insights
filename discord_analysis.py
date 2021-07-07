
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        print(f'Connected to {guild.name}')
    channels = client.get_all_channels()
    channel = client.get_channel(861874864473767969)
    messages = await channel.history(limit=123).flatten()
    for message in messages:
        print(message.content)


client.run(TOKEN)