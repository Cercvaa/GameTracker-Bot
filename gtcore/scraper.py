import discord,asyncio,requests,bs4,re,tabulate,sqlite3
from tabulate import tabulate
from bs4 import BeautifulSoup

class GTcore():
    def __init__(self, ip):
        self.ip = ip
        self.page = requests.get("https://www.gametracker.com/server_info/" + self.ip)
        self.soup = BeautifulSoup(self.page.content, "html.parser")

    def banner(self):
        image = self.soup.find("img", class_="item_560x95")
        return image['src']
    
    def checkip(self):
        errors = list()

        for error in self.soup.find_all("div", class_="blocknewhdr"):
            errors.append(error.text.strip())

        if errors[0] == "We could not find the server you requested." or errors[0] == "The server you requested is not in the GameTracker database.":
            return False
        else: return True

    def map(self):
        map_text = self.soup.find('div', class_="si_map_header").text.strip()

        return map_text

    def mapimage(self):

        image = self.soup.find("img", class_="item_160x120")
        return image['src']

    def maps(self):

        g = list()
        for image in self.soup.find_all("img", class_="item_260x170"):
            g.append(image['src'])

        return g[1]

    def rank_image(self):

        g = list()
        for image in self.soup.find_all("img", class_="item_260x170"):
            g.append(image['src'])

        return g[2]

    def name(self):
        h = self.soup.find("span", class_="blocknewheadertitle").text.strip()

        return h

    def players(self):
        spans = list()
        for span in self.soup.find_all("span", id = True):
            spans.append(span.text)

        players = spans[0]
        return players

    def rank(self):
        ranks = list()
        ranks1 = self.soup.find_all("span", class_="item_color_title")
        for rank in ranks1:
            rank = rank.next_sibling
            ranks.append(rank.strip())

        rank_finnaly = ''
        text = ranks[7]
        text1 = text.replace('(', '')

        text2 = ranks[12]
        text2_ = text2.replace('(', '')
        if len(text1) > len(text2_):
            rank_finnaly = text1
        else:
            rank_finnaly = text2_

        return rank_finnaly

    def status(self):

        try:
            status = self.soup.find("span", class_="item_color_success").text.strip()
            if status == "Alive" : statusi = "🟢 **Active**"
            else: statusi = "🔴 **Offline**"
            return statusi
        except AttributeError:
            return "--"


    def playersrefresher(self):
        pl = list()
        for player in self.soup.find_all("a", href = re.compile("^/player")):
            pl.append(player.text.strip())

        table = self.soup.find("table", class_="table_lst table_lst_stp")
        
        scores = list()
        rows = table.find_all("tr")
        for tr in rows:
            td = tr.find_all("td")[2]
            scores.append(td.text.strip())
        scores.pop(0)

        time_played = list()
        rows = table.find_all("tr")
        for tr in rows:
            td = tr.find_all("td")[3]
            time_played.append(td.text.strip())
        time_played.pop(0)

        headers = ["Name", "Score", "Time Played"]
        make_table = zip(pl, scores, time_played)
        return tabulate(make_table, headers = headers)


    def scan(self):
        scanned = self.soup.find("div", class_="item_float_right item_text_12").text.strip()
        return scanned

    def servermanager(self):
        a = self.soup.find("div", class_="block630_content_left")
        names = list()
        for links in a.find_all("a", href = True):
                    names.append(links.string)
        servermanager = " ".join(names[2].split())
        return servermanager

    def variable(self, ip : str):
        page = requests.get(f"https://www.gametracker.com/server_info/{ip}/server_variables/")
        soup = BeautifulSoup(page.content, "html.parser")
        values = list()
        for aleko in soup.find_all("a", href = re.compile("^/search/")):
            values.append(aleko.text.strip())

        n = len(values)
        tb = soup.find("table", class_="table_lst table_lst_gse")
        rows = tb.find_all("tr")

        mgeli = list()
        for tr in rows:
            td = tr.find_all("td")[0]
            mgeli.append(td.text.strip())

        values.remove(values[0])
        values.pop()

        table = zip(mgeli, values)
        headers = ["Values", "Variables"]
        return tabulate(table, headers=headers)

    def top10(self, ip : str):
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

        headers = ["Name", "Score", "Time Played", "Score/Min"]
        table = zip(players, scores, time, scores_min)
        return tabulate(table, headers=headers)

