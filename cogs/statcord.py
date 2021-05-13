import discord,statcord
from discord.ext import commands

client = commands.AutoShardedBot(command_prefix = ">")

class Statcord(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.key = ""
        self.api = statcord.Client(self.client, self.key)
        self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self,ctx):
        if ctx.author.id == 481341632478707727:
            return
        else:
            self.api.command_run(ctx)



def setup(client):
    client.add_cog(Statcord(client))
