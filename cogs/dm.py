import discord 
from discord.ext import commands

client = commands.AutoShardedBot(command_prefix=">")


class DM(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        guild = message.guild
        if not guild:
            channel = self.client.get_channel(813111657256583210)
            await channel.send("DM: {0.author.name} : {0.content}".format(message))


def setup(client):
    client.add_cog(DM(client))