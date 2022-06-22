import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import etree
from numpy import datetime64
import csv

today = datetime64(datetime.now())
item_name_scmlink = {'★ Karambit | Gamma Doppler (Factory New)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Gamma%20Doppler%20%28Factory%20New%29', 'start': '2021-06-14', 'end': today},
 '★ Karambit | Lore (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Lore%20%28Field-Tested%29', 'start': '2021-03-07', 'end': today},
 '★ Skeleton Knife | Slaughter (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Skeleton%20Knife%20%7C%20Slaughter%20%28Minimal%20Wear%29', 'start': '2022-02-01', 'end': today},
 '★ Stiletto Knife | Doppler (Factory New)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Stiletto%20Knife%20%7C%20Doppler%20%28Factory%20New%29','start': '2021-01-01', 'end': today},
 '★ StatTrak™ Karambit | Lore (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20StatTrak%E2%84%A2%20Karambit%20%7C%20Lore%20%28Field-Tested%29','start': '2021-07-02', 'end': today},
 '★ M9 Bayonet | Lore (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20M9%20Bayonet%20%7C%20Lore%20%28Field-Tested%29','start': '2021-09-17', 'end': today},
 '★ Karambit | Autotronic (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Autotronic%20%28Field-Tested%29','start': '2021-07-16', 'end': today},
 '★ M9 Bayonet | Damascus Steel (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20M9%20Bayonet%20%7C%20Damascus%20Steel%20%28Field-Tested%29','start': '2021-04-13', 'end': '2022-04-25'},
 '★ Karambit | Forest DDPAT (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Forest%20DDPAT%20%28Field-Tested%29','start': '2021-08-15', 'end': today},
 '★ Bayonet | Freehand (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Bayonet%20%7C%20Freehand%20%28Field-Tested%29','start': '2021-04-23', 'end': today},
 '★ StatTrak™ M9 Bayonet | Stained (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20StatTrak%E2%84%A2%20M9%20Bayonet%20%7C%20Stained%20%28Minimal%20Wear%29','start': '2021-10-01', 'end': today},
 '★ Karambit | Urban Masked (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Urban%20Masked%20%28Field-Tested%29','start': '2021-08-15', 'end': today},
 '★ Bayonet | Black Laminate (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Bayonet%20%7C%20Black%20Laminate%20%28Minimal%20Wear%29', 'start': '2021-09-11', 'end': today},
 '★ Skeleton Knife | Urban Masked (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Skeleton%20Knife%20%7C%20Urban%20Masked%20%28Field-Tested%29','start': '2021-09-11', 'end': today},
 '★ Karambit | Boreal Forest (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Boreal%20Forest%20%28Field-Tested%29','start': '2021-07-17', 'end': '2022-04-30'},
 '★ Talon Knife | Damascus Steel (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Talon%20Knife%20%7C%20Damascus%20Steel%20%28Minimal%20Wear%29','start': '2021-06-17', 'end': '2022-03-10'},
 '★ Skeleton Knife | Forest DDPAT (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Skeleton%20Knife%20%7C%20Forest%20DDPAT%20%28Minimal%20Wear%29', 'start': '2021-09-11', 'end': today},
 '★ Talon Knife | Stained (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Talon%20Knife%20%7C%20Stained%20%28Minimal%20Wear%29', 'start': '2021-09-18', 'end': today},
 '★ Talon Knife | Blue Steel (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Talon%20Knife%20%7C%20Blue%20Steel%20%28Minimal%20Wear%29', 'start': '2021-08-15', 'end': '2022-03-10'},
 '★ Karambit | Scorched (Minimal Wear)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Karambit%20%7C%20Scorched%20%28Minimal%20Wear%29', 'start': '2021-09-15', 'end': '2022-04-27'},
 'AWP | Containment Breach (Field-Tested)': {'link': 'https://steamcommunity.com/market/listings/730/AWP%20%7C%20Containment%20Breach%20%28Field-Tested%29', 'start': '2021-01-01', 'end': today},
 '★ Talon Knife | Marble Fade (Factory New)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Talon%20Knife%20%7C%20Marble%20Fade%20%28Factory%20New%29', 'start': '2021-06-26', 'end': '2021-09-03'},
 '★ Huntsman Knife | Marble Fade (Factory New)': {'link': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Huntsman%20Knife%20%7C%20Marble%20Fade%20%28Factory%20New%29', 'start': '2021-05-22', 'end': '2021-06-08'}}


def update_values():
    """erstellt für jedes Item eine CSV Datei mit den Values für jeden Tag"""
    for item in item_name_scmlink.items():
        itemname = item[0]
        websitedata = requests.get(item[1]['link'])
        data = BeautifulSoup(websitedata.text)
        dom = etree.HTML(str(data))
        # Command, um die Liste zu bekommen. Diese wird, da sie eine Liste an Listen ist, mit
        # 2 Eckigen Klammern begonnen und beendet.
        content2 = dom.xpath('//*[@id="responsive_page_template_content"]/script[2]')[0].text.split("line1")[1].split("[[")[1].split("]]")[0]

        with open(f"item_values_by_date/{itemname}.csv", "w", newline='') as f:
            writer = csv.writer(f, delimiter='§', escapechar="", quoting=csv.QUOTE_NONE)
            for entry in content2.split("],["):
                # für die letzten 30 Tage sind für jede Stunde die Preise gespeichert.
                # Deshalb werden nur die Preise um 1 Uhr genommen, da an allen anderen Tagen nur
                # die Preise um 1 Uhr gespeichert sind.
                if [entry] != entry.split("01:"):
                    writer.writerow([entry[1:-1].replace("\"", "")])

if __name__ == '__main__':
    #update_values()
    df = pd.read_csv('/Users/timehmann/Documents/Programmieren/VSCode/Python/SmallProjects/Info_Project/item_values_by_date/★ Bayonet | Black Laminate (Minimal Wear).csv', names=["Date", "Value", "TradingVolume"])
    print(df.head())
    df['Date']=df['Date'].apply(lambda x: x[:-7])
    df['Date']=df['Date'].apply(lambda x: datetime.strftime(datetime.strptime(x, '%b %d %Y'), '%Y-%m-%d'))
    df['rolling_avg'] = df['Value'].rolling(window=5, min_periods=1).mean()
    print(df.head(n=10))
