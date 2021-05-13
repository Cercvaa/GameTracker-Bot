import discord,dbl
from discord.ext import commands

client = commands.AutoShardedBot(command_prefix = ">")


class TopGG(commands.Cog):
    """
    This example uses dblpy's webhook system.
    In order to run the webhook, at least webhook_port must be specified (number between 1024 and 49151).
    """

    def __init__(self, client):
        self.client = client
        self.token = ""  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.client, self.token, webhook_path='/dblwebhook', webhook_auth='password', webhook_port=5000, autopost = True)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        """An event that is called whenever someone votes for the bot on top.gg."""
        print("Received an upvote:", "\n", data, sep="")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        print("Received a test upvote:", "\n", data, sep="")



def setup(client):
    client.add_cog(TopGG(client))
