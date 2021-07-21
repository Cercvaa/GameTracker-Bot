import discord,requests,re,bs4,os,psycopg2,datetime,tabulate,googlesearch
from googlesearch import search
from datetime import datetime
from tabulate import tabulate
from bs4 import BeautifulSoup
from discord.ext import commands
from gtcore import scraper

DATABASE_URL = ""

conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
c = conn.cursor()

client = commands.AutoShardedBot(command_prefix=">")
c.execute("CREATE TABLE IF NOT EXISTS costumers(name TEXT, ipname TEXT, guild_id TEXT);")
conn.commit()


class core(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name=f"with >help | gametrackerbot.cf"))

    @commands.command()
    async def setname(self, ctx, p : str, *, ipname : str):
        conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
        c = conn.cursor()
        core = scraper.GTcore(p)
        if core.checkip() == True:
            setn = list()
            count = 0

            c.execute(f"SELECT ipname FROM costumers WHERE guild_id = '{ctx.guild.id}'")
            results = c.fetchall()

            for result in results:
                setn.append(result[0])

            for i in range(len(setn)):
                if ipname == setn[i]:
                    count += 1

            if count == 1:
                await ctx.send(f"```{ipname} is already set```")
            else:
                await ctx.send(f"```ip: {p}\nipname: {ipname}```")
                insert = (f"INSERT INTO costumers VALUES('{p}', '{ipname}', '{ctx.guild.id}')")
                c.execute(insert)
                conn.commit()
        else:
            await ctx.send("The ip you requested is not in the GameTracker database.")

    @setname.error
    async def setname_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write ip address and ipname. ex: >setname 127.1232.1242:3456 gaming**")

    @commands.command()
    async def clear(self, ctx):
        conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
        c = conn.cursor()
        c.execute(f"SELECT * FROM costumers WHERE guild_id = '{ctx.guild.id}'")
        c.execute("DELETE FROM costumers")
        conn.commit()
        await ctx.send("```Queue is cleared.```")

    @commands.command()
    async def queue(self, ctx):
        conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
        c = conn.cursor()
        query_list_1 = list()
        query_list_2 = list()
        c.execute(f"SELECT * FROM costumers WHERE guild_id = '{ctx.guild.id}'")
        conn.commit()
        results = c.fetchall()
        for result in results:
            query_list_1.append(str(result[0]))
            query_list_2.append(str(result[1]))
        table = zip(query_list_1, query_list_2)
        headers = ["ip","ipname"]
        await ctx.send(f"```{tabulate(table, headers=headers)}```")
        

    @commands.command()
    async def info(self, ctx, *, ip : str):
        conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
        c = conn.cursor()
        c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
        result = c.fetchone()
        conn.commit()
        if result is not None:
            core = scraper.GTcore(result[0])
            title = core.name()
            banner = core.banner()
            scanned = core.scan()
            servermanager = core.servermanager()

            embed = discord.Embed(title = title, color = 0x2F3136)
            embed.add_field(name = "Server Manager:", value = servermanager)
            embed.set_image(url = "https:" + banner)
            embed.set_footer(text = scanned)
            await ctx.send(embed = embed)
        else: 
            core = scraper.GTcore(ip)
            if core.checkip() == False:
                await ctx.send("The server you requested is not in the GameTracker database.")
            else:
                title = core.name()
                banner = core.banner()
                scanned = core.scan()
                servermanager = core.servermanager()

                embed = discord.Embed(title = title, color = 0x2F3136)
                embed.add_field(name = "Server Manager:", value = servermanager)
                embed.set_image(url = "https:" + banner)
                embed.set_footer(text = scanned)
                await ctx.send(embed = embed)

    @info.error 
    async def info_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write server ip. ex: >info 123.125.1245:2331**")


    @commands.command(aliases = ['cm'])
    async def currentmap(self, ctx, *, ip : str):
        conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
        c = conn.cursor()
        c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
        result = c.fetchone()
        conn.commit()
        if result is not None:
            core = scraper.GTcore(result[0])
            title = core.name()
            map = core.map()
            map_image = core.mapimage()
            scanned = core.scan()
            
            embed = discord.Embed(title = title, description = f"`{map}`", color = 0x2F3136)
            embed.set_image(url = "https:" + map_image)
            embed.set_footer(text = scanned)
            await ctx.send(embed = embed)

            if map_image == "//image.gametracker.com/images/maps/160x120/nomap.jpg":
                message = await ctx.send(f"{ctx.author.mention}, Do you want to search image ?")
                first = "✔️"
                second = "❌"
                await message.add_reaction(first)
                await message.add_reaction(second)
                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in [first,second]
                react, user = await self.client.wait_for("reaction_add", check=check)
                if react.emoji == first:
                    map_search = search(map, num_results=1)
                    await ctx.send(map_search[0])
                else:
                    await ctx.channel.purge(limit = 1)
        else:
            core = scraper.GTcore(ip)
            if core.checkip() == False:
                await ctx.send("The server you requested is not in the GameTracker database.")
            else:
                title = core.name()
                map = core.map()
                map_image = core.mapimage()
                scanned = core.scan()
                
                embed = discord.Embed(title = title, description = f"`{map}`", color = 0x2F3136)
                embed.set_image(url = "https:" + map_image)
                embed.set_footer(text = scanned)
                await ctx.send(embed = embed)

                if map_image == "//image.gametracker.com/images/maps/160x120/nomap.jpg":
                    message = await ctx.send(f"{ctx.author.mention}, Do you want to search image ?")
                    first = "✔️"
                    second = "❌"
                    await message.add_reaction(first)
                    await message.add_reaction(second)
                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in [first,second]
                    react, user = await self.client.wait_for("reaction_add", check=check)
                    if react.emoji == first:
                        map_search = search(map, num_results=1)
                        await ctx.send(map_search[0])
                    else:
                        await ctx.channel.purge(limit = 1)


            
    @currentmap.error 
    async def currentmap_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write server ip**")

    @commands.command()
    async def maps(self, ctx, *, ip : str):
        conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
        c = conn.cursor()
        c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
        result = c.fetchone()
        conn.commit()

        if result is not None:
            core = scraper.GTcore(result[0])
            title = core.name()
            maps = core.maps()
            scanned = core.scan()

            embed = discord.Embed(title = title, description = f"``Favorite Maps``", color = 0x2F3136)
            embed.set_image(url = "https:" + maps)
            embed.set_footer(text = scanned)
            await ctx.send(embed = embed)
        else:
            core = scraper.GTcore(ip)
            if core.checkip() == False:
                await ctx.send("The server you requested is not in the GameTracker database.")
            else:
                title = core.name()
                maps = core.maps()
                scanned = core.scan()

                embed = discord.Embed(title = title, description = f"``Favorite Maps``", color = 0x2F3136)
                embed.set_image(url = "https:" + maps)
                embed.set_footer(text = scanned)
                await ctx.send(embed = embed)
    
    @maps.error 
    async def maps_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write server ip**")

    @commands.command(aliases = ['ranks'])
    async def rank(self, ctx, *, ip : str):
        conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
        c = conn.cursor()
        c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
        result = c.fetchone()
        conn.commit()

        if result is not None:
            core = scraper.GTcore(result[0])
            title = core.name()
            scanned = core.scan()
            rankimage = core.rank_image()
            
            embed = discord.Embed(title = title, description = "``Server Rank``", color = 0x2F3136)
            embed.set_image(url = "https:" + rankimage)
            embed.set_footer(text = scanned)
            await ctx.send(embed = embed)
        else:
            core = scraper.GTcore(ip)
            if core.checkip() == False:
                await ctx.send("The server you requested is not in the GameTracker database.")
            else:
                title = core.name()
                scanned = core.scan()
                rankimage = core.rank_image()
                
                embed = discord.Embed(title = title, description = "``Server Rank``", color = 0x2F3136)
                embed.set_image(url = "https:" + rankimage)
                embed.set_footer(text = scanned)
                await ctx.send(embed = embed)


    @rank.error 
    async def rank_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write server ip**")



    @commands.command()
    async def top10(self, ctx, *, ip : str):
        conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
        c = conn.cursor()
        c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
        result = c.fetchone()
        conn.commit()

        if result is not None:
            core = scraper.GTcore(result[0])
            top = core.top10(result[0])
            await ctx.send(f"```{top}```")
        else:
            core = scraper.GTcore(ip)
            if core.checkip() == False:
                await ctx.send("The server you requested is not in the GameTracker database.")
            else:
                top = core.top10(ip)
                await ctx.send(f"```{top}```")

    @top10.error
    async def top10_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write server ip**")

    @commands.command(aliases = ['pi'])
    async def playerinfo(self, ctx, ip : str, *, name : str):
        try:
            c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
            mgeli = c.fetchone()
            result_1 = str(mgeli[0])
            page = requests.get(f"https://www.gametracker.com/player/{name}/{result_1}/")
            soup = BeautifulSoup(page.content, "html.parser")
            image = soup.find("img", id = "banner_560x95")
            embed = discord.Embed(title = name, color = 0x2F3136)
            embed.set_image(url = f"https:{image['src']}")
            await ctx.send(embed = embed)
        except TypeError:
            page = requests.get(f"https://www.gametracker.com/player/{name}/{ip}/")
            soup = BeautifulSoup(page.content, "html.parser")

            error = soup.find("div", class_="blocknewhdr")

            if error.text.strip() == "We could not find the server you requested.":
                await ctx.send("We could not find the player name you requested.")
            else:
                page = requests.get(f"https://www.gametracker.com/player/{name}/{ip}/")
                soup = BeautifulSoup(page.content, "html.parser")
                name = soup.find("span", class_="blocknewheadertitle").text 
                image = soup.find("img", id = "banner_560x95")
                embed = discord.Embed(title = name.strip(), color = 0x2F3136)
                embed.set_image(url = f"https:{image['src']}")
                await ctx.send(embed = embed)

    @playerinfo.error
    async def playerinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write server ip and name**")

    @commands.command(aliases = ['ps'])
    async def playerscore(self, ctx, ip : str, *, name : str):
        try:
            c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
            mgeli = c.fetchone()
            result_1 = str(mgeli[0])
            page = requests.get(f"https://www.gametracker.com/player/{name}/{result_1}/")
            soup = BeautifulSoup(page.content, "html.parser")

            graph_player_score = soup.find("img", id = "graph_player_score")
            embed = discord.Embed(title = name, color = 0x2F3136)
            embed.set_image(url = f"https:{graph_player_score['src']}")
            await ctx.send(embed = embed)
        except TypeError:
            page = requests.get(f"https://www.gametracker.com/player/{name}/{ip}/")
            soup = BeautifulSoup(page.content, "html.parser")

            error = soup.find("div", class_="blocknewhdr")

            if error.text.strip() == "We could not find the server you requested.":
                await ctx.send("We could not find the player name you requested.")
            else:
                page = requests.get(f"https://www.gametracker.com/player/{name}/{ip}/")
                soup = BeautifulSoup(page.content, "html.parser")

                graph_player_score = soup.find("img", id = "graph_player_score")
                embed = discord.Embed(title = name, color = 0x2F3136)
                embed.set_image(url = f"https:{graph_player_score['src']}")
                await ctx.send(embed = embed)

    @playerscore.error 
    async def playerscore_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write server ip and name**")
    
    @commands.command(aliases = ['pt'])
    async def playertime(self, ctx, ip : str, *, name : str):
        try:
            c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
            mgeli = c.fetchone()
            result_1 = str(mgeli[0])
            page = requests.get(f"https://www.gametracker.com/player/{name}/{result_1}/")
            soup = BeautifulSoup(page.content, "html.parser")

            graph_player_time = soup.find("img", id = "graph_player_time")
            embed = discord.Embed(title = name, color = 0x2F3136)
            embed.set_image(url=f"https:{graph_player_time['src']}")
            await ctx.send(embed = embed)
        except TypeError:
            page = requests.get(f"https://www.gametracker.com/player/{name}/{ip}/")
            soup = BeautifulSoup(page.content, "html.parser")

            error = soup.find("div", class_="blocknewhdr")

            if error.text.strip() == "We could not find the server you requested.":
                await ctx.send("We could not find the player name you requested.")
            else:
                page = requests.get(f"https://www.gametracker.com/player/{name}/{ip}/")
                soup = BeautifulSoup(page.content, "html.parser")

                graph_player_time = soup.find("img", id = "graph_player_time")
                embed = discord.Embed(title = name, color = 0x2F3136)
                embed.set_image(url=f"https:{graph_player_time['src']}")
                await ctx.send(embed = embed)

    @playertime.error 
    async def playertime_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write server ip and name**")

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title = "Help", description = "``See All Commands Usage``[Here](https://gametrackerbot.cf/commands.html).", color = 0x2F3136)
        embed.add_field(name = "Commands:", value = "`>info,>rank,>maps,>top10,>setname,>queue,>clear,>playerinfo,>playerscore,>playertime,>bug`")
        embed.add_field(name = "<:gt2:852514074151616512> New GameTracker", value = "**GameTracker Pro is already online, invite it from [here](https://discordbotlist.com/bots/gametracker-pro)**", inline = False)
        embed.add_field(name = "Links", value="[Server](https://discord.gg/KxWNFJdAsY) | [See video](https://www.youtube.com/watch?v=F4oPVzY-zcg) | [See Website](https://gametrackerbot.cf/) | [Invite](https://discord.com/oauth2/authorize?client_id=787358079498453052&permissions=456768&scope=bot)", inline = False)
        embed.set_footer(text="Bot made by Cercva#4848", icon_url="https://cdn.discordapp.com/avatars/481341632478707727/a_544e33ec02ff27cea89101fa42ce9809.webp?size=256")
        await ctx.send(embed = embed)


    @commands.command()
    async def bug(self, ctx, *, bug_info : str):
        user = ctx.author
        user_photo = user.avatar_url
        channel = client.get_channel(812413226172022814)
        now = datetime.now()
        dro = now.strftime("%m/%d/%Y, %H:%M:%S")
        embed = discord.Embed(title = "```Bug```", description = bug_info, colour = discord.Colour.red())
        embed.set_thumbnail(url=user_photo)
        embed.add_field(name = "User id:", value=f"```{user.id}```")
        embed.set_footer(text = f"მესიჯი გამოაგზავნა: {user}, გამოგზავნის დრო: {dro}")
        await channel.send(embed = embed)
        await channel.send("<@481341632478707727>")
        await ctx.send(f"**{ctx.author.mention}, Your message has been sent to the developer.**")

    @bug.error
    async def bug_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(">bug write bug")

    @commands.command()
    @commands.is_owner()
    async def send(self, ctx,  id : int, *, message : str):
        user = self.client.get_user(id)
        await user.send(message)
        await ctx.send(f"```მესიჯი გაეგზვნა: {user}```")  

    @send.error
    async def send_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("არ გაქვს მაგის უფლება.")


def setup(client):
    client.add_cog(core(client))
