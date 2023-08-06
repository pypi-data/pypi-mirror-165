import requests
from bs4 import BeautifulSoup

def GameData():
    from datetime import datetime
    try:
        from pytz import timezone
    except:
        return("pytz not detected! please install pytz!")
    Data = {
        "Online_User": "",
        "WOTDLink" : "",
        "WOTDName" : "",
        "GTTime" : "",
        "GTDate" : ""
    }
    try:
        Website = requests.get(f"https://www.growtopiagame.com/detail").json()

        Data["Online_User"] = Website["online_user"]
        Data["WOTDLink"] = Website["world_day_images"]["full_size"] 
        Data["WOTDName"] = ((Data["WOTDLink"].replace('https://www.growtopiagame.com/worlds/','')).replace('.png','')).upper()
        Data["GTTime"] = datetime.now(timezone('UTC')).astimezone(timezone('America/New_York')).strftime("%X")
        Data["GTDate"] = datetime.now(timezone('UTC')).astimezone(timezone('America/New_York')).strftime("%x")
        return Data
    except: 
        return("It looks like we can't reach growtopiagame.com")

def ItemData(NameItem):
    Result = {}
    try:
        try:
            ItemFinder = requests.get(f"https://growtopia.fandom.com/api/v1/SearchSuggestions/List?query={NameItem}").json()
            ItemPage = requests.get("https://growtopia.fandom.com/wiki/{}".format(ItemFinder["items"][0]["title"]))
            HTMLResult = BeautifulSoup(ItemPage.text, "html.parser")
            Properties = HTMLResult.find_all('div',  class_= "card-text")
            Data = HTMLResult.find('table', class_= "card-field")
            Rarity = BeautifulSoup((str((HTMLResult.find('small'))).replace("(Rarity: ", "")).replace(")", ""), "html.parser").text
            try:
                Result.update({"Rarity": int(Rarity)})
            except:
                Result.update({"Rarity": "None"})
            PropertiesResult = []
            for add in Properties:
                hum = BeautifulSoup(str(add).replace("<br/>", "\n"), "html.parser")
                PropertiesResult.append(((hum)).text)
            Result.update({"Description": PropertiesResult[0].strip()})
            Result.update({"Properties": PropertiesResult[1].strip()})

            DataResult = []
            for typ in Data:
                mus = BeautifulSoup((str(typ).replace("</tr>", ",")).replace("</th>", ","), "html.parser")
                DataResult = (((mus.text).split(",")))
            res = 0 
            while res <= (len(DataResult)-3):
                Result.update({DataResult[res].strip(): DataResult[res+1].strip()})
                res = res+2
            return Result
        except:
            return("It looks like we can't reach fandom.com")
    except:
        return("Sorry! I can't find",NameItem,"in Growtopia Fandom")

def ItemRecipe(NameItem):
    try:
        try:
            ItemFinder = requests.get(f"https://growtopia.fandom.com/api/v1/SearchSuggestions/List?query={NameItem}").json()
            ItemPage = requests.get("https://growtopia.fandom.com/wiki/{}".format(ItemFinder["items"][0]["title"]))
            HTMLResult = BeautifulSoup(ItemPage.text, "html.parser")
            Recipe = {}
            ws = 0
            wd = len(HTMLResult.select(".content"))
            for item in HTMLResult.select(".content"):
                if wd == ws:
                    break
                if item.select(".content") == []:
                    if wd == ws:
                        break
                    Recipe[((item.find('th')).text).strip()] = (str(((BeautifulSoup(((str(item.select('td')).replace("</td>", "space")).replace("</li>", "space")).replace("<span>", "space"), "html.parser").get_text(' ', strip=True)).replace("space", "")).replace("\n", "")).strip())
                    ws +=1
                else:
                    meh = ((item.find('th')).text).strip()
                    Recipe[meh] = {}
                    if item.select(".content"):
                        wd -= 1
                        for mes in item.select(".content"):
                            Recipe[meh][((mes.find('th')).text).strip()] = (str(((BeautifulSoup(((str(mes.select('td')).replace("</td>", "space")).replace("</li>", "space")).replace("</span>", "space"), "html.parser").get_text(' ', strip=True)).replace("space", "")).replace("\n", "")).strip())
                            ws +=1
            return Recipe
        except:
            return("It looks like we can't reach fandom.com")
    except:
        return("Sorry! I can't find",NameItem,"in Growtopia Fandom")

def ItemSprite(NameItem):
    try:
        Data = {
        "Item" :"",
        "Tree" :"",
        "Seed" :""
        }
        try:
            ItemFinder = requests.get(f"https://growtopia.fandom.com/api/v1/SearchSuggestions/List?query={NameItem}").json()
            sprite = BeautifulSoup(requests.get("https://growtopia.fandom.com/wiki/{}".format(ItemFinder["items"][0]["title"])).text, "html.parser")
        except:
            print("It looks like we can't reach fandom.com")
        images = sprite.find('div', {"class": "gtw-card"})
        Data["Item"]= (images.find('div', {"class": "card-header"})).img['src']
        Data["Tree"] = (((((((images.find_next('td')).find_next('td')).find_next('td')).find_next('td')).find_next('td')).find_next('td')).find_next('td')).img['src']
        Data["Seed"] = (images.find('td', {"class": "seedColor"})).img['src']
        return Data
    except:
        return("Sorry! I can't find",NameItem,"in Growtopia Fandom")