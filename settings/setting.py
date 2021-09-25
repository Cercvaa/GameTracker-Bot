import sqlite3,json,mysql.connector

def checkdata(guild : int):
    conn = mysql.connector(
        host = HOST, 
        user = USER, 
        passwd = PASSWD,
        database = DATABASE
    )
    c = conn.cursor()


    count = 0

    c.execute(f"SELECT ipname FROM costumers WHERE guild_id = '{str(guild)}'")
    result = c.fetchall()

    if len(result) == 5:
        return False
    else: return True


def checklan(guild : int):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute(f"SELECT lan FROM language WHERE guild_id = '{str(guild)}'")
    lan = c.fetchone()

    if lan is not None and lan == "ge":
        return "ge"
    else:
        return False


def get_lang(lan : str, response : str):
    if lan == "ge":
        f = open('georgia.json', encoding="utf8")
        data = json.load(f)

        return data[response]
    elif lan == "en":
        f = open('default.json', encoding="utf8")
        data = json.load(f)


        return data[response]

