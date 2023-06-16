from deta import Deta
from cryptography.fernet import Fernet
from datetime import datetime
from dateutil import tz
import os
import random
import json
import re

deta = Deta(os.environ['DETA_PROJECT_KEY'])
fernet = Fernet(os.environ['ENCRYPTION_KEY'])
petsdata = deta.Base('pets')
playerdata = deta.Base('player')
logsdata = deta.Base('logs')

pets_type = ["dog", "cat", "bird"]

def extract_number_range(input_text):
    pattern = r"from (\d+) to (\d+)"
    matches = re.search(pattern, input_text)
    if matches:
        start = int(matches.group(1))
        end = int(matches.group(2))
        return (start, end)
    return None

def extract_items(input_text):
    pattern = r"choose (.+)"
    matches = re.search(pattern, input_text)
    if matches:
        items_string = matches.group(1)
        items = [item.strip() for item in items_string.split(",")]
        return items
    return None

class Pet():
    def __init__(self):
        pass

    def Decode(self, data: list):
        for i in range(len(data)):
            for x in data[i]['stats']:
                getBytes = data[i]['stats'][x][2:-1]
                data[i]['stats'][x] = fernet.decrypt(getBytes.encode()).decode('utf-8')
            for x in data[i]['status']:
                getBytes = data[i]['status'][x][2:-1]
                data[i]['status'][x] = fernet.decrypt(getBytes.encode()).decode('utf-8')
            for x in data[i]['skills']:
                getBytes = data[i]['skills'][x][2:-1]
                data[i]['skills'][x] = fernet.decrypt(getBytes.encode()).decode('utf-8')
        return data

    def check(self):
        fetchData = petsdata.fetch().items
        if fetchData:
            fetchData = self.Decode(fetchData)
            for i in range(len(fetchData)):
                local_timezone = tz.tzlocal()
                local_datetime = datetime.now(local_timezone)
                getDTObject = datetime.strptime(fetchData[i]['stats']["last_interacted"], "%Y-%m-%d %H:%M:%S %z")
                difference = local_datetime - getDTObject
                difference = int(difference.total_seconds())
                formatted_datetime = local_datetime.strftime("%Y-%m-%d %H:%M:%S %z")
                hunger = int(fetchData[i]["status"]['hunger'])
                hygiene = int(fetchData[i]["status"]['hygiene'])
                fun = int(fetchData[i]["status"]['fun'])
                love = int(fetchData[i]["status"]['love'])
                mood = int(fetchData[i]["status"]['mood'])
                exp = int(fetchData[i]["stats"]['exp'])
                level = int(fetchData[i]["stats"]['level'])
                if exp > 100:
                    level += 1
                    exp = 0
                if difference > 300:
                    hunger -= min((difference // 300), hunger)
                    hygiene -= min((difference // 400), hygiene)
                    fun -= min((difference // 500), fun)
                    love -= min((difference // 600), love)
                    mood = int((hunger + hygiene + fun + love) / 4)
                if difference > 86400:
                    mood = 0
                if difference > 172800 and hunger <= 0 and hygiene <= 0 and fun <= 0 and love <= 0:
                    self.abandon(fetchData[i]['name'])
                    self.logs(fetchData[i]['name'] + " ran away because it felt neglected.")
                    return fetchData[i]['name'] + " ran away because it felt neglected."
                petsdata.update({
                    "status.hunger": str(fernet.encrypt(str(hunger).encode())),
                    "status.hygiene": str(fernet.encrypt(str(hygiene).encode())),
                    "status.fun": str(fernet.encrypt(str(fun).encode())),
                    "status.love": str(fernet.encrypt(str(love).encode())),
                    "status.mood": str(fernet.encrypt(str(mood).encode())),
                    "stats.exp": str(fernet.encrypt(str(exp).encode())),
                    "stats.level": str(fernet.encrypt(str(level).encode())),
                    "stats.prestige": str(fernet.encrypt(fetchData[i]['stats']['prestige'].encode())),
                    "stats.last_interacted": str(fernet.encrypt(formatted_datetime.encode()))
                }, fetchData[i]['key'])
            return fetchData
        return []


    def adopt(self, type: str, name: str):
        try:
            if type in pets_type:
                fetchData = petsdata.fetch().items
                if fetchData:
                    self.check()
                    return "You have already adopted a pet!"
                local_timezone = tz.tzlocal()
                local_datetime = datetime.now(local_timezone)
                formatted_datetime = local_datetime.strftime("%Y-%m-%d %H:%M:%S %z")
                petsdata.put({
                    "type": type,
                    "name": name,
                    "form": "0001",
                    "status": {
                        "hunger": str(fernet.encrypt("100".encode())),
                        "hygiene": str(fernet.encrypt("100".encode())),
                        "fun": str(fernet.encrypt("100".encode())),
                        "love": str(fernet.encrypt("100".encode())),
                        "mood": str(fernet.encrypt("100".encode()))
                    },
                    "stats": {
                        "exp": str(fernet.encrypt("0".encode())),
                        "level": str(fernet.encrypt("0".encode())),
                        "prestige": str(fernet.encrypt("0".encode())),
                        "adopted_on": str(fernet.encrypt(formatted_datetime.encode())),
                        "last_interacted": str(fernet.encrypt(formatted_datetime.encode()))
                    },
                    "skills": {
                        "sustainability": str(fernet.encrypt("0".encode())),
                        "hunting": str(fernet.encrypt("0".encode()))
                    }
                })
                self.logs(f"Adopted a {type} named {name}.")
                return f"Adopted {name}!"
            else:
                return f"{type} is not available for adoption."
        except:
            return "Something went wrong"
    
    def view(self):
        fetchData = petsdata.fetch().items
        if fetchData:
            for i in range(len(fetchData)):
                fetchData[i].pop("key")
                fetchData[i].pop("type")
                fetchData[i].pop("skills")
                for x in fetchData[0]['stats']:
                    getBytes = fetchData[i]['stats'][x][2:-1]
                    fetchData[i]['stats'][x] = fernet.decrypt(getBytes.encode()).decode('utf-8')
                for x in fetchData[0]['status']:
                    getBytes = fetchData[0]['status'][x][2:-1]
                    fetchData[i]['status'][x] = fernet.decrypt(getBytes.encode()).decode('utf-8')
            return fetchData
        else:
            return "No pets found. Maybe try adopting one."
        
    def abandon(self, name: str):
        fetchData = petsdata.fetch({"name": name}).items
        if fetchData:
            key = fetchData[0]["key"]
            petsdata.delete(key)
            self.logs(f"Abandoned {name}.")
            return f"{name} has been abandoned :("
        else:
            return f"{name} not found."

    def pet(self):
        fetchData = petsdata.fetch().items
        if fetchData:
            self.check()
            fetchData = self.Decode(fetchData)
            for i in range(len(fetchData)):
                love = int(fetchData[i]["status"]['love'])
                if love < 90:
                    add_exp = int(fetchData[i]["stats"]['exp']) + random.randint(1, 5)
                    love += min((100 - love), random.randint(10, 30))
                    petsdata.update({
                        "status.love": str(fernet.encrypt(str(love).encode())),
                        "stats.exp": str(fernet.encrypt(str(add_exp).encode()))
                    }, fetchData[i]["key"])
                    return f'Petted {fetchData[i]["name"]}.'
                else:
                    return f'{fetchData[i]["name"]} feels very loved <3'
            return "Something went wrong"
        else:
            return "No pets found. Maybe try adopting one."
        
    def feed(self):
        fetchData = petsdata.fetch().items
        if fetchData:
            self.check()
            fetchData = self.Decode(fetchData)
            for i in range(len(fetchData)):
                hunger = int(fetchData[i]["status"]['hunger'])
                if hunger < 90:
                    add_exp = int(fetchData[i]["stats"]['exp']) + random.randint(1, 5)
                    hunger += min((100 - hunger), random.randint(10, 30))
                    petsdata.update({
                        "status.hunger": str(fernet.encrypt(str(hunger).encode())),
                        "stats.exp": str(fernet.encrypt(str(add_exp).encode()))
                    }, fetchData[i]["key"])
                    return f'Fed {fetchData[i]["name"]}.'
                else:
                    return f'{fetchData[i]["name"]} is feeling full and does not want to eat.'
            return "Something went wrong"
        else:
            return "No pets found. Maybe try adopting one."

    def wash(self):
        fetchData = petsdata.fetch().items
        if fetchData:
            self.check()
            fetchData = self.Decode(fetchData)
            for i in range(len(fetchData)):
                hygiene = int(fetchData[i]["status"]['hygiene'])
                if hygiene < 90:
                    add_exp = int(fetchData[i]["stats"]['exp']) + random.randint(1, 5)
                    hygiene += min((100 - hygiene), random.randint(10, 30))
                    petsdata.update({
                        "status.hygiene": str(fernet.encrypt(str(hygiene).encode())),
                        "stats.exp": str(fernet.encrypt(str(add_exp).encode()))
                    }, fetchData[i]["key"])
                    return f'Washed {fetchData[i]["name"]}.'
                else:
                    return f'{fetchData[i]["name"]} is already clean!'
            return "Something went wrong"
        else:
            return "No pets found. Maybe try adopting one."
    
    def play(self):
        fetchData = petsdata.fetch().items
        if fetchData:
            self.check()
            fetchData = self.Decode(fetchData)
            for i in range(len(fetchData)):
                fun = int(fetchData[i]["status"]['fun'])
                if fun < 90:
                    add_exp = int(fetchData[i]["stats"]['exp']) + random.randint(1, 5)
                    fun += min((100 - fun), random.randint(10, 30))
                    petsdata.update({
                        "status.fun": str(fernet.encrypt(str(fun).encode())),
                        "stats.exp": str(fernet.encrypt(str(add_exp).encode()))
                    }, fetchData[i]["key"])
                    return f'Played with {fetchData[i]["name"]}.'
                else:
                    return f'{fetchData[i]["name"]} does not want to get too high.'
            return "Something went wrong"
        else:
            return "No pets found. Maybe try adopting one."
    
    def talk(self, text: str):
        fetchData = petsdata.fetch().items
        if fetchData:
            try:
                text = text.replace("!", "").replace("?", "")
                if "random number" in text:
                    number_range = extract_number_range(text)
                    if number_range:
                        start, end = number_range
                        num = random.randint(start, end)
                        return f'{fetchData[0]["name"]} chooses {num}!'
                    else:
                        return f'{fetchData[0]["name"]} is confused with the numbers.'
                if "choose" in text:
                    items = extract_items(text)
                    if items:
                        chosen = random.choice(items)
                        return f'{fetchData[0]["name"]} chooses {chosen}!'
                    else:
                        return f'{fetchData[0]["name"]} has no idea what to choose.'
                f = open('response.json')
                resp = json.load(f)
                reply = resp[fetchData[0]["type"]][text] 
                return f'{fetchData[0]["name"]}: {reply}'
            except:
                return f'{fetchData[0]["name"]} ignores you.'
        else:
            return "No pets to talk to. Maybe try adopting one."

    def logs(self, detail: str):
        local_timezone = tz.tzlocal()
        local_datetime = datetime.now(local_timezone)
        formatted_datetime = local_datetime.strftime("%Y-%m-%d %H:%M:%S %z")
        logsdata.put({
            "timestamp": formatted_datetime,
            "details": detail
        })
        return "Logged"