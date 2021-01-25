import discord
import os
import logging
from dotenv import load_dotenv
from discord.ext import commands, tasks
from itertools import cycle

dir_path = os.path.dirname(os.path.realpath(__file__))

load_dotenv()
BOT_KEY = os.getenv("BOT_KEY")

intents = discord.Intents.all()

client = commands.Bot(command_prefix='.', intents=intents)
status = cycle(['.info', '.rumor', '.report'])

#logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Send me some Rumors!'))

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print(f'{extension} loaded')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    print(f'{extension} unloaded')


@client.command()
async def reload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
    except:
        print(f'{extension} wasnt currently loaded')
    client.load_extension(f'cogs.{extension}')
    print(f'{extension} loaded')


cogs = dir_path + r'/cogs'

for filename in os.listdir(cogs):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(BOT_KEY)
