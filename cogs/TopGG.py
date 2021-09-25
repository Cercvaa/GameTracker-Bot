import hikari,lightbulb,dbl


bot = lightbulb.Bot(
    token = TOKEN, #change it
    prefix = ">",
    intents = hikari.Intents.ALL
)

class UpdateServers(lightbulb.Plugin):

    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc4NzM1ODA3OTQ5ODQ1MzA1MiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjExNDE1NDgwfQ.OYMNEvEvBy-87UGBOAlf9_GhglcpBOgNZRFUlJHOcnc"  # set this to your DBL token
    dblpy = dbl.DBLClient(bot, token, webhook_path='/dblwebhook', webhook_auth='password', webhook_port=5000, autopost = True)



def load(bot):
    bot.add_plugin(UpdateServers())