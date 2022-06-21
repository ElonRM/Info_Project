import requests
from bs4 import BeautifulSoup
from lxml import etree
import csv

item_name_scmlink = {'★ Karambit | Gamma Doppler (Factory New)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Gamma%20Doppler%20%28Factory%20New%29', 'start': '2021-06-14', 'end': None},
 '★ Karambit | Lore (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Lore%20%28Field-Tested%29', 'start': '2021-03-07', 'end': None},
 '★ Skeleton Knife | Slaughter (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Skeleton%20Knife%20%7C%20Slaughter%20%28Minimal%20Wear%29', 'start': '', 'end': ''},
 '★ Stiletto Knife | Doppler (Factory New)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Stiletto%20Knife%20%7C%20Doppler%20%28Factory%20New%29','start': '', 'end': ''},
 '★ StatTrak™ Karambit | Lore (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20StatTrak%E2%84%A2%20Karambit%20%7C%20Lore%20%28Field-Tested%29','start': '', 'end': ''},
 '★ M9 Bayonet | Lore (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20M9%20Bayonet%20%7C%20Lore%20%28Field-Tested%29','start': '', 'end': ''},
 '★ Karambit | Autotronic (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Autotronic%20%28Field-Tested%29','start': '', 'end': ''},
 '★ M9 Bayonet | Damascus Steel (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20M9%20Bayonet%20%7C%20Damascus%20Steel%20%28Field-Tested%29','start': '2021-04-13', 'end': ''},
 '★ Karambit | Forest DDPAT (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Forest%20DDPAT%20%28Field-Tested%29','start': '', 'end': ''},
 '★ Bayonet | Freehand (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Bayonet%20%7C%20Freehand%20%28Field-Tested%29','start': '2021-04-23', 'end': ''},
 '★ StatTrak™ M9 Bayonet | Stained (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20StatTrak%E2%84%A2%20M9%20Bayonet%20%7C%20Stained%20%28Minimal%20Wear%29','start': '', 'end': ''},
 '★ Karambit | Urban Masked (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Urban%20Masked%20%28Field-Tested%29','start': '', 'end': ''},
 '★ Bayonet | Black Laminate (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Bayonet%20%7C%20Black%20Laminate%20%28Minimal%20Wear%29', 'start': '', 'end': ''},
 '★ Skeleton Knife | Urban Masked (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Skeleton%20Knife%20%7C%20Urban%20Masked%20%28Field-Tested%29','start': '', 'end': ''},
 '★ Karambit | Boreal Forest (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Boreal%20Forest%20%28Field-Tested%29','start': '', 'end': ''},
 '★ Talon Knife | Damascus Steel (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Talon%20Knife%20%7C%20Damascus%20Steel%20%28Minimal%20Wear%29','start': '', 'end': ''},
 '★ Skeleton Knife | Forest DDPAT (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Skeleton%20Knife%20%7C%20Forest%20DDPAT%20%28Minimal%20Wear%29', 'start': '', 'end': ''},
 '★ Talon Knife | Stained (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Talon%20Knife%20%7C%20Stained%20%28Minimal%20Wear%29', 'start': '', 'end': ''},
 '★ Talon Knife | Blue Steel (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Talon%20Knife%20%7C%20Blue%20Steel%20%28Minimal%20Wear%29', 'start': '', 'end': ''},
 '★ Karambit | Scorched (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Scorched%20%28Minimal%20Wear%29', 'start': '', 'end': ''},
 'AWP | Containment Breach (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/AWP%20%7C%20Containment%20Breach%20%28Field-Tested%29', 'start': '', 'end': ''},
 '★ Talon Knife | Marble Fade (Factory New)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Talon%20Knife%20%7C%20Marble%20Fade%20%28Factory%20New%29', 'start': '', 'end': ''},
 '★ Huntsman Knife | Marble Fade (Factory New)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Huntsman%20Knife%20%7C%20Marble%20Fade%20%28Factory%20New%29', 'start': '2021-05-22', 'end': ''}}


params = {'country': 'DE', 'currency': 3, 'appid': 730, 'market_hash_name': 'Falchion%20Case'}
cookie = {'SteamLogin': '76561198803945915%7C%7C05B20631DB8F994299F3D61640804A7BBD249D70'}
data = requests.get('http://steamcommunity.com/market/pricehistory/?country=US&currency=1&appid=730&market_hash_name=Falchion%20Case', cookies=cookie)
print(data.text)


for item in item_name_scmlink.items():
    itemname = item[0]
    websitedata = requests.get(item[1]['link'])
    data = BeautifulSoup(websitedata.text)
    #content = data.find(id="responsive_page_template_content")

    dom = etree.HTML(str(data))
    content2 = dom.xpath('//*[@id="responsive_page_template_content"]/script[2]')[0].text.split("line1")[1].split("[[")[1].split("]]")[0]

    with open(f"item_values_by_date/{itemname}.csv", "w", newline='') as f:
        writer = csv.writer(f, delimiter='§', escapechar="", quoting=csv.QUOTE_NONE)
        for entry in content2.split("],["):
            if [entry] != entry.split("01:"):
                writer.writerow([entry[1:-1].replace("\"", "")])




