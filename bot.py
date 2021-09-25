import logging,lightbulb,hikari,os,mysql.connector
from os import environ, listdir
from config import TOKEN,HOST,USER,PASSWD,DATABASE

conn = mysql.connector.connect(
    host = HOST, 
    user = USER, 
    passwd = PASSWD,
    database = DATABASE
)

c.execute("CREATE TABLE IF NOT EXISTS costumers(ip TEXT, ipname TEXT, guild_id TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS language(lan TEXT, guild_id TEXT)")
conn.commit()

bot = lightbulb.Bot(
    token = TOKEN, #change it
    prefix = ">",
    intents = hikari.Intents.ALL
)
bot.remove_command("help")
print(bot.heartbeat())

for filename in listdir('./cogs'):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(
    activity=hikari.Activity(name = ">help | gametrackerbot.cf", type = hikari.ActivityType.PLAYING), 
    asyncio_debug=True
)

