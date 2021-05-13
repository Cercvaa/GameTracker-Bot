import discord,os
from os import environ, listdir
from discord.ext import commands

client = commands.AutoShardedBot(command_prefix=">")
client.remove_command("help")

TOKEN = ""

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


for filename in listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run(TOKEN)
