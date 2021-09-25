import lightbulb,hikari,statcord

bot = lightbulb.Bot(
    token = TOKEN, #change it
    prefix = ">",
    intents = hikari.Intents.ALL
)

class Statcord(lightbulb.Plugin):
    
    key = "statcord.com-5i9oCYz6hXYlooTQYQd7"
    api = statcord.Client(bot, self.key)
    api.start_loop()

    
    
    async def on_command(self, ctx):
        if ctx.author.id == 481341632478707727:
            return
        else:
            api.command_run(ctx)


def load(bot):
    bot.add_plugin(Statcord())