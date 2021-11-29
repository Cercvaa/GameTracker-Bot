import hikari,lightbulb,mysql.connector,tabulate,json
from tabulate import tabulate
from settings.setting import checkdata, checklan, get_lang
from lightbulb.events import CommandErrorEvent
from config import PREFIX,TOKEN,HOST,USER,PASSWD,DATABASE,COLOR
from gtcore import scraper

languages = ['ge', 'en', 'ru']

class Database(lightbulb.Plugin):

    @lightbulb.command()
    async def lang(self, ctx, lan : str):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()
        
        if lan not in languages:
            embed = hikari.Embed(title = "Available Languages", description = "``ge``, ``en``, ``ru``", color = COLOR)
            await ctx.respond(embed = embed)
        elif lan in languages:
            c.execute(f"SELECT lan FROM language WHERE guild_id = '{ctx.get_guild().id}'")
            result = c.fetchone()

            if result is not None:
                c.execute(f"UPDATE language SET lan = {lan} WHERE guild_id = '{ctx.get_guild().id}'")
                conn.commit()
                await ctx.respond(f"language has been updated to ``{lan}``")
            else:
                c.execute(f"INSERT INTO language VALUES('{lan}', '{ctx.get_guild().id}')")
                conn.commit()
                await ctx.respond(f"language has been updated to ``{lan}``")

    @lightbulb.check(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
    @lightbulb.command()
    async def setname(self, ctx, ip : str, *, ipname : str):

        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()

        core = scraper.GTcore(ip)
        c.execute(f"SELECT lan FROM language WHERE guild_id = '{ctx.get_guild().id}'")
        lans = c.fetchone()  

        if lans is not None:
            lan = lans[0]
        else:
            lan = "en"
        
        if core.checkip() == True and checkdata(ctx.get_guild().id):
            setn = list()
            count = 0

            c.execute(f"SELECT ipname FROM costumers WHERE guild_id = '{ctx.get_guild().id}'")
            results = c.fetchall()


            for result in results:
                setn.append(result[0])

            for i in range(len(setn)):
                if ipname == setn[i]:
                    count += 1

            if count == 1:
                await ctx.respond(get_lang(lan, "setname_set"))
            else:
                await ctx.respond(f"```ip: {ip}\nipname: {ipname}```")
                insert = (f"INSERT INTO costumers VALUES('{ip}', '{ipname}', '{ctx.get_guild().id}')")
                c.execute(insert)
                conn.commit()
        elif core.checkip() == False:
            await ctx.respond(get_lang(lan, "ip_error"))
        elif checkdata(ctx.get_guild().id) == False:
            await ctx.respond(get_lang(lan, "server_limit"))

    @setname.command_error()
    async def on_setname_error(self, event):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()

        c.execute(f"SELECT lan FROM language WHERE guild_id = '{event.message.guild_id}'")
        result = c.fetchone()
        if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
            if result is None:
                embed = hikari.Embed(title = "❌ **Error**", description = "You need to write ip and ipname.", color = COLOR)
                return await event.message.respond(embed = embed)
            else:
                embed = hikari.Embed(title = get_lang(result[0], "error"), description = get_lang(result[0], "setname_error"), color = COLOR)
                return await event.message.respond(embed = embed)
        elif isinstance(event.exception, lightbulb.errors.MissingRequiredPermission):
            if result is None:
                embed = hikari.Embed(title = "❌ **Error**", description = "You don't have enough permissions to use command.")
                return await event.message.respond(embed = embed)

    @lightbulb.command()
    async def clear(self, ctx):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()
        

        c.execute(f"SELECT * FROM costumers WHERE guild_id = '{ctx.get_guild().id}'")
        c.execute("DELETE FROM costumers")
        c.execute(f"SELECT lan FROM language WHERE guild_id = '{ctx.get_guild().id}'")
        result = c.fetchone()
        conn.commit()
        if result is None: await ctx.respond("```Queue is cleared.```")  
        else: 
            await ctx.respond(get_lang(result[0], "clear_response"))


    @lightbulb.command(aliases = ["del"])
    async def delete(self, ctx, *, name : str):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()

        c.execute(f"SELECT ip FROM costumers WHERE guild_id = '{ctx.get_guild().id}' AND ipname = '{name}'")
        result = c.fetchone()
        c.execute(f"SELECT lan FROM language WHERE guild_id = '{ctx.get_guild().id}'")
        lang = c.fetchone()

        if result is not None:
            c.execute(f"DELETE FROM costumers WHERE guild_id = '{ctx.get_guild().id}' AND ipname = '{name}'")
            conn.commit()
            await ctx.respond(get_lang("en", "delete_response_success").format("``" + name + "``") if lang is None else get_lang(lang[0], "delete_response_success").format("``" + name + "``"))
            
        else:
            await ctx.respond(get_lang("en", "delete_response_error").format("``" + name + "``") if lang is None else get_lang(lang[0], "delete_response_error").format("``" + name + "``"))

    
    @delete.command_error()
    async def on_delete_error(self, event):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()

        c.execute(f"SELECT lan FROM language WHERE guild_id = '{event.message.guild_id}'")
        result = c.fetchone()

        if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
            if result is not None:
                embed = hikari.Embed(title = get_lang(result[0], "error"), description = get_lang(result[0], "delete_error"), color = COLOR)
                return await event.message.respond(embed = embed)
            else:
                embed = hikari.Embed(title = "❌ **Error**", description = "You need to write ip name.", color = COLOR)
                return await event.message.respond(embed = embed)

            
    
    @lightbulb.command()
    async def queue(self, ctx):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()


        query_list_1 = list()
        query_list_2 = list()
        c.execute(f"SELECT * FROM costumers WHERE guild_id = '{ctx.get_guild().id}'")
        results = c.fetchall()
        conn.commit()
        for result in results:
            query_list_1.append(str(result[0]))
            query_list_2.append(str(result[1]))
        table = zip(query_list_1, query_list_2)
        headers = ["ip","ipname"]
        await ctx.respond(f"```{tabulate(table, headers=headers)}```")



def load(bot):
    bot.add_plugin(Database())

def unload(bot):
    bot.remove_plugin("Database")
