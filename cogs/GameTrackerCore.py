import discord,requests,re,bs4,os,psycopg2,datetime,tabulate,googlesearch
from googlesearch import search
from datetime import datetime
from tabulate import tabulate
from bs4 import BeautifulSoup
from discord.ext import commands

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

    @setname.error
    async def setname_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write ip address and ipname. ex: >setname 127.1232.1242:3456 gaming**")

    @commands.command()
    async def clear(self, ctx):
        c.execute(f"SELECT * FROM costumers WHERE guild_id = '{ctx.guild.id}'")
        c.execute("DELETE FROM costumers")
        await ctx.send("```Queue is cleared.```")

    @commands.command()
    async def queue(self, ctx):
        query_list_1 = list()
        query_list_2 = list()
        c.execute(f"SELECT * FROM costumers WHERE guild_id = '{ctx.guild.id}'")
        results = c.fetchall()
        for result in results:
            query_list_1.append(str(result[0]))
            query_list_2.append(str(result[1]))
        table = zip(query_list_1, query_list_2)
        headers = ["ip","ipname"]
        await ctx.send(f"```{tabulate(table, headers=headers)}```")

    @commands.command()
    async def info(self, ctx, *, ip : str):
        try:
            c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
            mgeli = c.fetchone()
            result_1 = str(mgeli[0])
            names = list()
            page = requests.get("https://www.gametracker.com/server_info/" + result_1)
            soup = BeautifulSoup(page.content, "html.parser")
            title = soup.find("span", class_="blocknewheadertitle").text.strip()
            a = soup.find("div", class_="block630_content_left")
            scanned = soup.find("div", class_="item_float_right item_text_12").text.strip()
            for links in a.find_all("a", href = True):
                names.append(links.string)
            servermanager = " ".join(names[2].split())
            images = soup.find("img", class_="item_560x95")
            embed = discord.Embed(title = title, color = 0x2F3136)
            embed.add_field(name = "Server Manager:", value = servermanager)
            embed.set_image(url = "https:" + images['src'])
            embed.set_footer(text = scanned)
            await ctx.send(embed = embed)
        except TypeError:
            page = requests.get(f"https://www.gametracker.com/server_info/{ip}")
            soup = BeautifulSoup(page.content, "html.parser")
            errors = list()

            for error in soup.find_all("div", class_="blocknewhdr"):
                errors.append(error.text.strip())

            if errors[0] == "We could not find the server you requested." or errors[0] == "The server you requested is not in the GameTracker database.":
                await ctx.send("We could not find the server you requested.")
            else:
                names = list()
                page = requests.get("https://www.gametracker.com/server_info/" + ip)
                soup = BeautifulSoup(page.content, "html.parser")
                title = soup.find("span", class_="blocknewheadertitle").text.strip()
                a = soup.find("div", class_="block630_content_left")
                scanned = soup.find("div", class_="item_float_right item_text_12").text.strip()
                for links in a.find_all("a", href = True):
                    names.append(links.string)
                servermanager = " ".join(names[2].split())
                images = soup.find("img", class_="item_560x95")
                embed = discord.Embed(title = title, color = 0x2F3136)
                embed.add_field(name = "Server Manager:", value = servermanager)
                embed.set_image(url = "https:" + images['src'])
                embed.set_footer(text = scanned)
                await ctx.send(embed = embed)

    @info.error 
    async def info_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write server ip. ex: >info 123.125.1245:2331**")


    @commands.command(aliases = ['cm'])
    async def currentmap(self, ctx, *, ip : str):
        try:
            c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
            mgeli = c.fetchone()
            result_1 = str(mgeli[0])
            page = requests.get("https://www.gametracker.com/server_info/" + result_1)
            soup = BeautifulSoup(page.content, "html.parser")
            title = soup.find("span", class_="blocknewheadertitle").text.strip()
            z = soup.find("div", class_="si_map_header").text.strip()
            scanned = soup.find("div", class_="item_float_right item_text_12").text.strip()
            image = soup.find("img", class_="item_160x120")
            embed = discord.Embed(title = title, description = f"`{z}   `", color = 0x2F3136)
            embed.set_image(url = "https:" + image['src'])
            embed.set_footer(text = scanned)
            await ctx.send(embed = embed)

            if image['src'] == "//image.gametracker.com/images/maps/160x120/nomap.jpg":
                message = await ctx.send(f"{ctx.author.mention}, Do you want to search image ?")
                first = "✔️"
                second = "❌"
                await message.add_reaction(first)
                await message.add_reaction(second)
                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in [first,second]
                react, user = await self.client.wait_for("reaction_add", check=check)
                if react.emoji == first:
                    map_search = search(z, num_results=1)
                    await ctx.send(map_search[0])
                else:
                    await ctx.channel.purge(limit = 1)
        except TypeError:
            page = requests.get(f"https://www.gametracker.com/server_info/{ip}")
            soup = BeautifulSoup(page.content, "html.parser")
            errors = list()

            for error in soup.find_all("div", class_="blocknewhdr"):
                errors.append(error.text.strip())

            if errors[0] == "We could not find the server you requested." or errors[0] == "The server you requested is not in the GameTracker database.":
                await ctx.send("We could not find the server you requested.")
            else:
                page = requests.get("https://www.gametracker.com/server_info/" + ip)
                soup = BeautifulSoup(page.content, "html.parser")
                title = soup.find("span", class_="blocknewheadertitle").text.strip()
                z = soup.find("div", class_="si_map_header").text.strip()
                scanned = soup.find("div", class_="item_float_right item_text_12").text.strip()
                image = soup.find("img", class_="item_160x120")
                embed = discord.Embed(title = title, description = f"`{z}`", color = 0x2F3136)
                embed.set_image(url = "https:" + image['src'])
                embed.set_footer(text = scanned)
                await ctx.send(embed = embed)
                if image['src'] == "//image.gametracker.com/images/maps/160x120/nomap.jpg":
                    message = await ctx.send(f"{ctx.author.mention}, Do you want to search image ?")
                    first = "✔️"
                    second = "❌"
                    await message.add_reaction(first)
                    await message.add_reaction(second)
                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in [first,second]
                    react, user = await self.client.wait_for("reaction_add", check=check)
                    if react.emoji == first:
                        map_search = search(z, num_results=1)
                        await ctx.send(map_search[0])
                    else:
                        await ctx.channel.purge(limit = 1)
            
    @currentmap.error 
    async def currentmap_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write server ip**")

    @commands.command()
    async def maps(self, ctx, *, ip : str):
        try:
            c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
            mgeli = c.fetchone()
            result_1 = str(mgeli[0])
            page = requests.get("https://www.gametracker.com/server_info/" + result_1)
            soup = BeautifulSoup(page.content, "html.parser")
            h = soup.find("span", class_="blocknewheadertitle").text
            title = " ".join(h.split())
            g = list()
            for image in soup.find_all("img", class_="item_260x170"):
                g.append(image['src'])

            scanned = soup.find("div", class_="item_float_right item_text_12").text.strip()

            embed = discord.Embed(title = title, description = "`Favorite Maps`", color = 0x2F3136)
            embed.set_image(url = "https:"+g[1])
            embed.set_footer(text = scanned)
            await ctx.send(embed = embed)
        except TypeError:
            page = requests.get(f"https://www.gametracker.com/server_info/{ip}")
            soup = BeautifulSoup(page.content, "html.parser")
            errors = list()

            for error in soup.find_all("div", class_="blocknewhdr"):
                errors.append(error.text.strip())

            if errors[0] == "We could not find the server you requested." or errors[0] == "The server you requested is not in the GameTracker database.":
                await ctx.send("We could not find the server you requested.")
            else:
                page = requests.get("https://www.gametracker.com/server_info/" + ip)
                soup = BeautifulSoup(page.content, "html.parser")
                h = soup.find("span", class_="blocknewheadertitle").text
                title = " ".join(h.split())
                g = list()
                for image in soup.find_all("img", class_="item_260x170"):
                    g.append(image['src'])

                scanned = soup.find("div", class_="item_float_right item_text_12").text.strip()

                embed = discord.Embed(title = title, description = "`Favorite Maps`", color = 0x2F3136)
                embed.set_image(url = "https:"+g[1])
                embed.set_footer(text = scanned)
                await ctx.send(embed = embed)
    
    @maps.error 
    async def maps_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write server ip**")

    @commands.command(aliases = ['ranks'])
    async def rank(self, ctx, *, ip : str):
        try: # Not Found
            c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
            mgeli = c.fetchone()
            result_1 = str(mgeli[0])
            page = requests.get("https://www.gametracker.com/server_info/" + result_1)
            soup = BeautifulSoup(page.content, "html.parser")
            title = soup.find("span", class_="blocknewheadertitle").text.strip()
            scanned = soup.find("div", class_="item_float_right item_text_12").text.strip()
            g = list()
            for image in soup.find_all("img", class_="item_260x170"):
                g.append(image['src'])
            embed = discord.Embed(title = title, description = "`Server Rank`", color = 0x2F3136)
            embed.set_image(url = "https:" + g[2])   
            embed.set_footer(text = scanned) 
            await ctx.send(embed = embed)
        except TypeError:
            page = requests.get(f"https://www.gametracker.com/server_info/{ip}")
            soup = BeautifulSoup(page.content, "html.parser")
            errors = list()

            for error in soup.find_all("div", class_="blocknewhdr"):
                errors.append(error.text.strip())

            if errors[0] == "We could not find the server you requested." or errors[0] == "The server you requested is not in the GameTracker database.":
                await ctx.send("We could not find the server you requested.")
            else:
                page = requests.get("https://www.gametracker.com/server_info/" + ip)
                soup = BeautifulSoup(page.content, "html.parser")
                title = soup.find("span", class_="blocknewheadertitle").text.strip()
                scanned = soup.find("div", class_="item_float_right item_text_12").text.strip()
                g = list()
                for image in soup.find_all("img", class_="item_260x170"):
                    g.append(image['src'])
                embed = discord.Embed(title = title, description = "`Server Rank`", color = 0x2F3136)
                embed.set_image(url = "https:" + g[2])   
                embed.set_footer(text = scanned) 
                await ctx.send(embed = embed)

    @rank.error 
    async def rank_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write server ip**")

    @commands.command()
    async def vars(self, ctx, *, ip : str):
        try:
            c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
            mgeli = c.fetchone()
            result_1 = str(mgeli[0])
            page = requests.get(f"https://www.gametracker.com/server_info/{result_1}/server_variables/")
            soup = BeautifulSoup(page.content, "html.parser")

            values = list()
            for aleko in soup.find_all("a", href = re.compile("^/search/")):
                values.append(aleko.text.strip())

            n = len(values)
            table = soup.find("table", class_="table_lst table_lst_gse")
            rows = table.find_all("tr")

            mgeli = list()
            for tr in rows:
                td = tr.find_all("td")[0]
                mgeli.append(td.text.strip())

            values.remove(values[0])
            values.pop()

            table = zip(mgeli, values)
            headers = ["Values", "Variables"]
            await ctx.send(f"```{tabulate(table, headers=headers)}```")
        except TypeError:
            page = requests.get(f"https://www.gametracker.com/server_info/{ip}")
            soup = BeautifulSoup(page.content, "html.parser")
            errors = list()

            for error in soup.find_all("div", class_="blocknewhdr"):
                errors.append(error.text.strip())

            if errors[0] == "We could not find the server you requested." or errors[0] == "The server you requested is not in the GameTracker database.":
                await ctx.send("We could not find the server you requested.")
            else:
                page = requests.get(f"https://www.gametracker.com/server_info/{ip}/server_variables/")
                soup = BeautifulSoup(page.content, "html.parser")

                values = list()
                for aleko in soup.find_all("a", href = re.compile("^/search/")):
                    values.append(aleko.text.strip())

                n = len(values)
                table = soup.find("table", class_="table_lst table_lst_gse")
                rows = table.find_all("tr")

                mgeli = list()
                for tr in rows:
                    td = tr.find_all("td")[0]
                    mgeli.append(td.text.strip())

                values.remove(values[0])
                values.pop()

                table = zip(mgeli, values)
                headers = ["Values", "Variables"]
                await ctx.send(f"```{tabulate(table, headers=headers)}```")
    
    @vars.error
    async def vars_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌**Write server ip**")

    @commands.command()
    async def top10(self, ctx, *, ip : str):
        try:
            c.execute(f"SELECT name FROM costumers WHERE guild_id = '{ctx.guild.id}' AND ipname = '{ip}'")
            mgeli = c.fetchone()
            result_1 = str(mgeli[0])
            page = requests.get(f"https://www.gametracker.com/server_info/{result_1}/top_players/")
            soup = BeautifulSoup(page.content, "html.parser")

            table = soup.find("table", class_="table_lst table_lst_spn")
            data = table.find("tbody")

            players = list()
            scores = list()
            time = list()
            scores_min = list()
            for aleko in soup.find_all("a", href = re.compile("^/player")):
                players.append(aleko.text.strip())

            rows = table.find_all("tr")

            for tr in rows:
                td = tr.find_all("td")[3]
                scores.append(td.text.strip())

            scores.remove(scores[0])
            scores.pop()

            for tr in rows:
                td = tr.find_all("td")[4]
                time.append(td.text.strip())

            time.remove(time[0])
            time.pop()

            for tr in rows:
                td = tr.find_all("td")[5]
                scores_min.append(td.text.strip())

            scores_min.remove(scores_min[0])
            scores_min.pop() 
            
            """
            embed = discord.Embed(title = "Top 10 Players", description = f"1.{players[0]}\n 2.{players[1]}\n 3.{players[2]}\n 4.{players[3]}\n 5.{players[4]}\n 6.{players[5]}\n 7.{players[6]}\n 8.{players[7]}\n 9.{players[8]}\n 10.{players[9]}", colour = discord.Colour.red())
            await ctx.send(embed = embed)
            for i in range(len(players)):
                print(players[i])
            """
            headers = ["Name", "Score", "Time Played", "Score/Min"]
            table = zip(players, scores, time, scores_min)
            await ctx.send(f"```{tabulate(table, headers=headers)}```")
        except TypeError:
            page = requests.get(f"https://www.gametracker.com/server_info/{ip}")
            soup = BeautifulSoup(page.content, "html.parser")
            errors = list()

            for error in soup.find_all("div", class_="blocknewhdr"):
                errors.append(error.text.strip())

            if errors[0] == "We could not find the server you requested." or errors[0] == "The server you requested is not in the GameTracker database.":
                await ctx.send("We could not find the server you requested.")
            else:

                page = requests.get(f"https://www.gametracker.com/server_info/{ip}/top_players/")
                soup = BeautifulSoup(page.content, "html.parser")

                table = soup.find("table", class_="table_lst table_lst_spn")
                data = table.find("tbody")

                players = list()
                scores = list()
                time = list()
                scores_min = list()
                for aleko in soup.find_all("a", href = re.compile("^/player")):
                    players.append(aleko.text.strip())

                rows = table.find_all("tr")

                for tr in rows:
                    td = tr.find_all("td")[3]
                    scores.append(td.text.strip())

                scores.remove(scores[0])
                scores.pop()

                for tr in rows:
                    td = tr.find_all("td")[4]
                    time.append(td.text.strip())

                time.remove(time[0])
                time.pop()

                for tr in rows:
                    td = tr.find_all("td")[5]
                    scores_min.append(td.text.strip())

                scores_min.remove(scores_min[0])
                scores_min.pop() 
                
                """
                embed = discord.Embed(title = "Top 10 Players", description = f"1.{players[0]}\n 2.{players[1]}\n 3.{players[2]}\n 4.{players[3]}\n 5.{players[4]}\n 6.{players[5]}\n 7.{players[6]}\n 8.{players[7]}\n 9.{players[8]}\n 10.{players[9]}", colour = discord.Colour.red())
                await ctx.send(embed = embed)
                for i in range(len(players)):
                    print(players[i])
                """
                headers = ["Name", "Score", "Time Played", "Score/Min"]
                table = zip(players, scores, time, scores_min)
                await ctx.send(f"```{tabulate(table, headers=headers)}```")

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
        embed.add_field(name = "Commands:", value = "`>info,>rank,>maps,>top10,>setname,>queue,>clear,>playerinfo,>playerscore,>playertime,>vars,>bug`")
        embed.add_field(name = "Links", value="[Server](https://discord.gg/f94Xmy9A) | [See video](https://www.youtube.com/watch?v=F4oPVzY-zcg) | [See Website](https://gametrackerbot.cf/) | [Invite](https://discord.com/oauth2/authorize?client_id=787358079498453052&permissions=456768&scope=bot)", inline = False)
        embed.set_footer(text="Bot made by Cercva#4848", icon_url="https://images-ext-1.discordapp.net/external/OI3w-IwvLo-oaNGi-lr-f2ndoP-V4A-WZga26_G6ogM/%3Fsize%3D128/https/cdn.discordapp.com/avatars/481341632478707727/343c038be27a9bd6680fa34d50eb2fd4.png")
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
