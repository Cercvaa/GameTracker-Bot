import lightbulb,tabulate,hikari,mysql.connector
from lightbulb.events import CommandErrorEvent
from tabulate import tabulate
from gtcore import scraper
from config import COLOR,HOST,USER,PASSWD,DATABASE
from settings.setting import checkdata, checklan, get_lang


class GT(lightbulb.Plugin):


    @lightbulb.listener(CommandErrorEvent)
    async def command_not_found(self, event):
        if isinstance(event.exception, lightbulb.errors.CommandNotFound):
            print("Unknown Command")

    
    @lightbulb.command()
    async def info(self, ctx, *, ip : str):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()

        c.execute(f"SELECT ip FROM costumers WHERE guild_id = '{ctx.get_guild().id}' AND ipname = '{ip}'")
        result = c.fetchone()
        c.execute(f"SELECT lan FROM language WHERE guild_id = '{ctx.get_guild().id}'")
        lang = c.fetchone()
        conn.commit()
        if result is not None:
            core = scraper.GTcore(result[0])
            title = core.name()
            banner = core.banner()
            scanned = core.scan()
            servermanager = core.servermanager()

            embed = hikari.Embed(title = title, color = COLOR)
            embed.add_field(name = "Server Manager:", value = servermanager)
            embed.set_image("https:"+ banner)
            embed.set_footer(text = scanned)
            await ctx.respond(embed = embed)
        else: 
            core = scraper.GTcore(ip)
            if core.checkip() == False:
                await ctx.respond(get_lang("en", "ip_error") if lang is None else get_lang(lang[0], "ip_error"))
            else:
                title = core.name()
                banner = core.banner()
                scanned = core.scan()
                servermanager = core.servermanager()

                embed = hikari.Embed(title = title, color = COLOR)
                embed.add_field(name = "Server Manager:", value = servermanager)
                embed.set_image("https:"+ banner)
                embed.set_footer(text = scanned)
                await ctx.respond(embed = embed)

    @info.command_error()
    async def on_info_error(self, event):
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
                embed = hikari.Embed(title = "❌ **Error**", description = "You need to write ip or ipname", color = COLOR)
                message = await event.message.respond(embed = embed)
                return message
            else:
                embed = hikari.Embed(title = get_lang(result[0], "error"), description = get_lang(result[0], "setname_error"), color = COLOR)
                message = await event.message.respond(embed = embed)
                return message



    @lightbulb.command(aliases = ['cm'])
    async def currentmap(self, ctx, *, ip : str):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()

        c.execute(f"SELECT ip FROM costumers WHERE guild_id = '{ctx.get_guild().id}' AND ipname = '{ip}'")
        result = c.fetchone()
        c.execute(f"SELECT lan FROM language WHERE guild_id = '{ctx.get_guild().id}'")
        lang = c.fetchone()
        conn.commit()
        if result is not None:
            core = scraper.GTcore(result[0])
            title = core.name()
            map = core.map()
            map_image = core.mapimage()
            scanned = core.scan()
            
            embed = hikari.Embed(title = title, description = f"`{map}`", color = COLOR)
            embed.set_image("https:" + map_image)
            embed.set_footer(text = scanned)
            message = await ctx.respond(embed = embed)
        else:
            core = scraper.GTcore(ip)
            if core.checkip() == False:
                await ctx.respond(get_lang("en", "ip_error") if lang is None else get_lang(lang[0], "ip_error"))
            else:
                title = core.name()
                map = core.map()
                map_image = core.mapimage()
                scanned = core.scan()
                
                embed = hikari.Embed(title = title, description = f"`{map}`", color = COLOR)
                embed.set_image("https:" + map_image)
                embed.set_footer(text = scanned)
                await ctx.respond(embed = embed)

    @currentmap.command_error()
    async def on_currentmap_error(self, event):
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
                embed = hikari.Embed(title = "❌ **Error**", description = "You need to write ip or ipname", color = COLOR)
                message = await event.message.respond(embed = embed)
                return message
            else:
                embed = hikari.Embed(title = get_lang(result[0], "error"), description = get_lang(result[0], "setname_error"), color = COLOR)
                message = await event.message.respond(embed = embed)
                return message

    @lightbulb.command()
    async def maps(self, ctx, *, ip : str):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()

        c.execute(f"SELECT ip FROM costumers WHERE guild_id = '{ctx.get_guild().id}' AND ipname = '{ip}'")
        result = c.fetchone()
        c.execute(f"SELECT lan FROM language WHERE guild_id = '{ctx.get_guild().id}'")
        lang = c.fetchone()
        conn.commit()

        if result is not None:
            core = scraper.GTcore(result[0])
            title = core.name()
            maps = core.maps()
            scanned = core.scan()

            embed = hikari.Embed(title = title, description = f"``Favorite Maps``", color = COLOR)
            embed.set_image("https:" + maps)
            embed.set_footer(text = scanned)
            await ctx.respond(embed = embed)
        else:
            core = scraper.GTcore(ip)
            if core.checkip() == False:
                await ctx.respond(get_lang("en", "ip_error") if lang is None else get_lang(lang[0], "ip_error"))
            else:
                title = core.name()
                maps = core.maps()
                scanned = core.scan()

                embed = hikari.Embed(title = title, description = f"``Favorite Maps``", color = COLOR)
                embed.set_image("https:" + maps)
                embed.set_footer(text = scanned)
                await ctx.respond(embed = embed)

    @maps.command_error()
    async def on_maps_error(self, event):
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
                embed = hikari.Embed(title = "❌ **Error**", description = "You need to write ip or ipname", color = COLOR)
                message = await event.message.respond(embed = embed)
                return message
            else:
                embed = hikari.Embed(title = get_lang(result[0], "error"), description = get_lang(result[0], "setname_error"), color = COLOR)
                message = await event.message.respond(embed = embed)
                return message


    @lightbulb.command(aliases = ['ranks'])
    async def rank(self, ctx, *, ip : str):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()

        c.execute(f"SELECT ip FROM costumers WHERE guild_id = '{ctx.get_guild().id}' AND ipname = '{ip}'")
        result = c.fetchone()
        c.execute(f"SELECT lan FROM language WHERE guild_id = '{ctx.get_guild().id}'")
        lang = c.fetchone()
        conn.commit()

        if result is not None:
            core = scraper.GTcore(result[0])
            title = core.name()
            scanned = core.scan()
            rankimage = core.rank_image()
            
            embed = hikari.Embed(title = title, description = "``Server Rank``", color = COLOR)
            embed.set_image("https:" + rankimage)
            embed.set_footer(text = scanned)
            await ctx.respond(embed = embed)
        else:
            core = scraper.GTcore(ip)
            if core.checkip() == False:
                await ctx.respond(get_lang("en", "ip_error") if lang is None else get_lang(lang[0], "ip_error"))
            else:
                title = core.name()
                scanned = core.scan()
                rankimage = core.rank_image()
                
                embed = hikari.Embed(title = title, description = "``Server Rank``", color = COLOR)
                embed.set_image("https:" + rankimage)
                embed.set_footer(text = scanned)
                await ctx.respond(embed = embed)

    @rank.command_error()
    async def on_rank_error(self, event):
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
                embed = hikari.Embed(title = "❌ **Error**", description = "You need to write ip or ipname", color = COLOR)
                message = await event.message.respond(embed = embed)
                return message
            else:
                embed = hikari.Embed(title = get_lang(result[0], "error"), description = get_lang(result[0], "setname_error"), color = COLOR)
                message = await event.message.respond(embed = embed)
                return message

    @lightbulb.command()
    async def top10(self, ctx, *, ip : str):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()

        c.execute(f"SELECT ip FROM costumers WHERE guild_id = '{ctx.get_guild().id}' AND ipname = '{ip}'")
        result = c.fetchone()
        c.execute(f"SELECT lan FROM language WHERE guild_id = '{ctx.get_guild().id}'")
        lang = c.fetchone()
        conn.commit()

        if result is not None:
            core = scraper.GTcore(result[0])
            top = core.top10(result[0])
            await ctx.respond(f"```{top}```")
        else:
            core = scraper.GTcore(ip)
            if core.checkip() == False:
                await ctx.respond(get_lang("en", "ip_error") if lang is None else get_lang(lang[0], "ip_error"))
            else:
                top = core.top10(ip)
                await ctx.respond(f"```{top}```")

    @top10.command_error()
    async def on_top10_error(self, event):
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
                embed = hikari.Embed(title = "❌ **Error**", description = "You need to write ip or ipname", color = COLOR)
                message = await event.message.respond(embed = embed)
                return message
            else:
                embed = hikari.Embed(title = get_lang(result[0], "error"), description = get_lang(result[0], "setname_error"), color = COLOR)
                message = await event.message.respond(embed = embed)
                return message


    @lightbulb.command(aliases = ['pi'])
    async def playerinfo(self, ctx, ip : str, *, name : str):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()
        

        c.execute(f"SELECT ip FROM costumers WHERE guild_id = '{ctx.get_guild().id}' AND ipname = '{ip}'")
        result = c.fetchone()
        c.execute(f"SELECT lan FROM language WHERE guild_id = '{ctx.get_guild().id}'")
        lang = c.fetchone()
        conn.commit()

        if result is not None:
            core = scraper.GTcore(result[0])
            playerbanner = core.player_banner(name)
            embed = hikari.Embed(title = name, color = COLOR)
            embed.set_image(f"https:{playerbanner}")
            await ctx.respond(embed = embed)
        else:
            core = scraper.GTcore(ip)
            if core.checkip() == False:
                await ctx.respond(get_lang("en", "player_response_error") if lang is None else get_lang(lang[0], "player_response_error"))
            else:
                core = scraper.GTcore(ip)
                playerbanner = core.player_banner(name)
                embed = hikari.Embed(title = name, color = COLOR)
                embed.set_image(f"https:{playerbanner}")
                await ctx.respond(embed = embed)

    @playerinfo.command_error()
    async def on_playerinfo_error(self, event):
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
                embed = hikari.Embed(title = "❌ **Error**", description="Write ip(ipname) and player name.", color = COLOR)
                return await event.message.respond(embed = embed)
            else:
                embed = hikari.Embed(title = get_lang(result[0], "error"), description=get_lang(result[0], "player_error"), color = COLOR)
                return await event.message.respond(embed = embed)
    
    @lightbulb.command(aliases = ["ps"])
    async def playerscore(self, ctx, ip : str, *, name : str):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()

        c.execute(f"SELECT ip FROM costumers WHERE guild_id = '{ctx.get_guild().id}' AND ipname = '{ip}'")
        mgeli = c.fetchone()
        c.execute(f"SELECT lan FROM language WHERE guild_id = '{ctx.get_guild().id}'")
        lang = c.fetchone()
        conn.commit()

        if mgeli is not None:
            core = scraper.GTcore(mgeli[0])
            graph_player_score = core.player_graph(name)
            embed = hikari.Embed(title = name, color = COLOR)
            embed.set_image(f"https:{graph_player_score}")
            await ctx.respond(embed = embed)
        else:
            core = scraper.GTcore(ip)
            if core.checkip() == False:
                await ctx.respond(get_lang("en", "player_response_error") if lang is None else get_lang(lang[0], "player_response_error"))
            else:
                core = scraper.GTcore(ip)
                graph_player_score = core.player_graph(name)
                embed = hikari.Embed(title = name, color = COLOR)
                embed.set_image(f"https:{graph_player_score}")
                await ctx.respond(embed = embed)

    @playerscore.command_error()
    async def on_playerscore_error(self, event):
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
                embed = hikari.Embed(title = "❌ **Error**", description="Write ip(ipname) and player name.", color = COLOR)
                return await event.message.respond(embed = embed)
            else:
                embed = hikari.Embed(title = get_lang(result[0], "error"), description=get_lang(result[0], "player_error"), color = COLOR)
                return await event.message.respond(embed = embed)

    
    @lightbulb.command(aliases = ['pt'])
    async def playertime(self, ctx, ip : str, *, name : str):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()
        c.execute(f"SELECT ip FROM costumers WHERE guild_id = '{ctx.get_guild().id}' AND ipname = '{ip}'")
        mgeli = c.fetchone()
        c.execute(f"SELECT lan FROM language WHERE guild_id = '{ctx.get_guild().id}'")
        lang = c.fetchone()
        conn.commit()
        if mgeli is not None:
            core = scraper.GTcore(mgeli[0])
            graph_player_time = core.player_time(name)
            embed = hikari.Embed(title = name, color = COLOR)
            embed.set_image(f"https:{graph_player_time}")
            await ctx.respond(embed = embed)
        else:
            core = scraper.GTcore(ip)
            if core.checkip() == False:
                await ctx.respond(get_lang("en", "player_response_error") if lang is None else get_lang(lang[0], "player_response_error"))
            else:
                graph_player_time = core.player_time(name)
                embed = hikari.Embed(title = name, color = COLOR)
                embed.set_image(f"https:{graph_player_time}")
                await ctx.respond(embed = embed)

    @playertime.command_error()
    async def on_playertime_error(self, event):
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
                embed = hikari.Embed(title = "❌ **Error**", description="Write ip(ipname) and player name.", color = COLOR)
                return await event.message.respond(embed = embed)
            else:
                embed = hikari.Embed(title = get_lang(result[0], "error"), description=get_lang(result[0], "player_error"), color = COLOR)
                return await event.message.respond(embed = embed)

    
    @lightbulb.command()
    async def top15(self, ctx, *, ip : str):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()
        c.execute(f"SELECT ip FROM costumers WHERE guild_id = '{ctx.get_guild().id}' AND ipname = '{ip}'")
        result = c.fetchone()
        conn.commit()
        if result is not None:
            server = scraper.GTcore(result[0])
            await ctx.respond(f"```{server.top15()}```")
        else:
            server = scraper.GTcore(ip)
            await ctx.respond(f"```{server.top15()}```")


    @top15.command_error()
    async def on_top15_error(self, event):
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
                embed = hikari.Embed(title = "❌ **Error**", description = "You need to write ip or ipname", color = COLOR)
                message = await event.message.respond(embed = embed)
                return message
            else:
                embed = hikari.Embed(title = get_lang(result[0], "error"), description = get_lang(result[0], "setname_error"), color = COLOR)
                message = await event.message.respond(embed = embed)
                return message

    @lightbulb.command()
    async def serverplayers(self, ctx, *, ip : str):
        conn = mysql.connector.connect(
            host = HOST, 
            user = USER, 
            passwd = PASSWD,
            database = DATABASE
        )
        c = conn.cursor()
        c.execute(f"SELECT ip FROM costumers WHERE guild_id = '{ctx.get_guild().id}' AND ipname = '{ip}'")
        result = c.fetchone()
        conn.commit()
        if result is not None:
            server = scraper.GTcore(result[0])
            if server.playersrefresher() == False:
                await ctx.respond("Error")
            else:
                await ctx.respond(f"```{server.playersrefresher()}```")
        elif result is None:
            server = scraper.GTcore(ip)
            if server.playersrefresher() == False:
                await ctx.respond("Error")
            else:
                await ctx.respond(f"```{server.playersrefresher()}```")

    @serverplayers.command_error()
    async def on_serverplayers_error(self, event):
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
                embed = hikari.Embed(title = "❌ **Error**", description = "You need to write ip or ipname", color = COLOR)
                message = await event.message.respond(embed = embed)
                return message
            else:
                embed = hikari.Embed(title = get_lang(result[0], "error"), description = get_lang(result[0], "setname_error"), color = COLOR)
                message = await event.message.respond(embed = embed)
                return message


    @lightbulb.command()
    async def help(self, ctx):
        embed = hikari.Embed(title = "Help", description = "``See All Commands Usage``[Here](https://gametrackerbot.cf/commands.html).", color = COLOR)
        embed.add_field(name = "Commands:", value = "``>info,>rank,>maps,>top10,>top15,>setname,>queue,>clear,>playerinfo,>playerscore,>playertime,>currentmap,>serverplayers,>delete,>lang``")
        embed.add_field(name = "Links", value="[Server](https://discord.gg/KxWNFJdAsY) | [See video](https://www.youtube.com/watch?v=F4oPVzY-zcg) | [See Website](https://gametrackerbot.cf/) | [Invite](https://discord.com/oauth2/authorize?client_id=787358079498453052&permissions=456768&scope=bot) | [Star this project](https://github.com/Cercvinatori/GameTracker-Bot)", inline = False)
        embed.set_footer(text="Bot made by Cercva#4848", icon="https://cdn.discordapp.com/avatars/481341632478707727/a_544e33ec02ff27cea89101fa42ce9809.webp?size=256")
        await ctx.respond(embed = embed)


def load(bot):
    bot.add_plugin(GT())


def unload(bot):
    bot.remove_plugin("GT")
