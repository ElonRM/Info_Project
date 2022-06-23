import csv
from pprint import pprint
from datetime import datetime
import matplotlib.pyplot as plt
from numpy import NaN
import pandas as pd
import math
import plotly.express as px

with open('rent_revenue_data.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

name_price_df = pd.read_csv('Einkaufspreise.csv', names=['Name', "Price"])

# entfernen der Kopfzeile
### [ID, DATE, ITEM, REVENUE]
data.pop(0)

# in rent_dict wird ein Dictionary erstellt, welches für jeden Skin (key) eine Liste
# der Renevue Entries beinhaltet (tuple aus tag und betrag)
# reverse für alt nach neu bei visualisierung, kann aber einfach ausgestellt werden
reverse = True
if reverse == True: data.reverse()

#print(data)
rent_dict = {}
# rent_dict hat den Namen eines Items als Key und eine Liste an Tupeln (date, revenue) als value
for revenue_entry in data:
    # revenue_entry ist ein Liste aus [ID, DATE, ITEM, REVENUE]
    try:
        rent_dict[revenue_entry[2]] = rent_dict[revenue_entry[2]] + [(revenue_entry[1], revenue_entry[3])]
    except Exception as e:
        #print(e)
        rent_dict[revenue_entry[2]] = [(revenue_entry[1], revenue_entry[3])]

# revenue_by_skin ist eine Liste für die summierte Einnahme pro Skin
revenue_by_skin=[(name, round(sum(float(entry[1]) for entry in val), 2)) for val, name in zip(rent_dict.values(), rent_dict.keys())]
revenue_by_skin.sort(key = lambda tup: tup[1], reverse = True)


def datediff(d1, d2):
    """gibt die Differenz zwischen 2 Tagen im Format D/M/Y zurück"""

    d1 = datetime.strptime(d1, "%d/%m/%Y")
    d2 = datetime.strptime(d2, "%d/%m/%Y")
    return abs((d2-d1).days)

# cumulated_revenue_by_rent_time ist ein Dictionary, welches für jeden Skin
# eine Liste bestehend aus der bis zu einem Vermietungseintrag Gesamteinnahmen und 
# den Vergangen Tagen beinhaltet
cumulated_revenue_by_rent_time={}
for val, name in zip(rent_dict.values(), rent_dict.keys()):
    # val ist ("date time", revenue), name ist Itemname
    if reverse == False: val.reverse()
    for entry in val:
        try:
            cumulated_revenue_by_rent_time[name]["revenue_history"] = cumulated_revenue_by_rent_time[name]["revenue_history"] + [(datediff(cumulated_revenue_by_rent_time[name]["start"], entry[0].split(" ")[0]), round(cumulated_revenue_by_rent_time[name]["revenue_history"][-1][-1] + float(entry[1]), 2))]
        except Exception as e:
            #print(e)
            cumulated_revenue_by_rent_time[name] = {"start": entry[0].split(" ")[0], "revenue_history":[(0,round(float(entry[1]), 2))]}

cumulated_revenue_by_rent_time_from_first={}
# cumulated_revenue_by_rent_time_from_first ist ein dictionary, welches für jedes Item die gesamte Revenue abhängig
# von der Anzahl an vergangen Tagen zu dem ältesten vermietungseintrag aller skins speichert. Die ältesten
# 7 skins werden ignoriert.
start = False
for val, name in zip(rent_dict.values(), rent_dict.keys()):
    # val ist ("date time", revenue), name ist Itemname
    # schneidet somit die ältesten 7 Items ab, da nach diesen über 7 Monate nichts kommt
    # Somit wird das Diagramm sehr viel übersichtlicher.
    # im Reverse Fall so, ansonsten break nach dem Namen.
    if name == "MP7 | Fade (Factory New)":
        start = True
        if reverse: continue
        else: break
    # da das Stiletto Knife Doppler noch vor der Mp7 Fade auftaucht.
    if start == True or name == "★ Stiletto Knife | Doppler (Factory New)":
        if reverse == False: val.reverse()
        for entry in val:
            try:
                cumulated_revenue_by_rent_time_from_first[name]["revenue_history"] = cumulated_revenue_by_rent_time_from_first[name]["revenue_history"] + [(datediff("18/01/2021", entry[0].split(" ")[0]), round(cumulated_revenue_by_rent_time_from_first[name]["revenue_history"][-1][-1] + float(entry[1]), 2))]
            except Exception as e:
                #print(e)
                cumulated_revenue_by_rent_time_from_first[name] = {"start": entry[0].split(" ")[0], "revenue_history":[(datediff("18/01/2021", entry[0].split(" ")[0]),round(float(entry[1]), 2))]}

#print(cumulated_revenue_by_rent_time["★ Karambit | Autotronic (Field-Tested)"])

xs = [x for x,_ in cumulated_revenue_by_rent_time["★ Karambit | Autotronic (Field-Tested)"]["revenue_history"]]
ys = [y for _,y in cumulated_revenue_by_rent_time["★ Karambit | Autotronic (Field-Tested)"]["revenue_history"]]


def analyse_revenue_by_type(includes_KGD: bool = True):
    """ Returns a dictionary with the knife type as the key and the revenue of the knife type as the value.
    includes_KGD decides whether the Karambit Gamma Doppler is part of the used Data Set as its rentting times are far off the mean"""
    # WARNING BAYONET IN M9-BAYONET
    types = ["Karambit", "★ Bayonet", "Huntsman", "M9 Bayonet", "Skeleton", "Stiletto"]
    revenue_by_type = [{type: round(sum(skin_revenue[1] for skin_revenue in revenue_by_skin if type in skin_revenue[0]), 2)} for type in types]
    if includes_KGD == False: revenue_by_type[0]["Karambit"] -= revenue_by_skin[0][1] # Fehler, falls KGP nicht das Item mit der höchsten revenue ist.

    return revenue_by_type

def get_calculated_return_per_year(name):

    revenue = cumulated_revenue_by_rent_time[name]['revenue_history'][-1][-1]
    dates = cumulated_revenue_by_rent_time[name]['revenue_history'][-1][0]
    price = float(name_price_df[name_price_df['Name'] == name]['Price'].sum())
    return ((365/dates*revenue)/price, dates, price) if price != 0 else (NaN, NaN, NaN)

def show_expected_revenue_per_year(df: pd.DataFrame):
    df['Trust']=df['Data_Size'].apply(lambda x: x**(1/2)/25)
    df['Category'] = df['Name'].apply(lambda x: x.replace('StatTrak™ ', '').split('|')[0])
    category_df = df.groupby(['Category']).mean().reset_index()

    fig1 = px.bar(df, x="Name", y="RPY", color = "Price", title="Expected ROI per Year").update_layout(font=dict(size=8))
    fig2 = px.bar(df, x="Name", y="RPY", color = "Trust", color_continuous_scale='Bluered_r', title="Expected ROI per Year").update_layout(font=dict(size=8))
    fig3 = px.bar(category_df, x="Category", y="RPY", color = "Trust", color_continuous_scale='Bluered_r', title="Expected ROI per Year").update_layout(font=dict(size=8))
    
    fig1.show()
    fig2.show()
    fig3.show()

return_per_year_df = pd.DataFrame(columns=['Name', 'RPY', 'Data_Size', 'Price'])
for skinname in cumulated_revenue_by_rent_time.keys():
    rpy, datasize, price = get_calculated_return_per_year(skinname)
    if not math.isnan(rpy):
        return_per_year_df.loc[len(return_per_year_df)] = [skinname, rpy, datasize, price]
        pass

show_expected_revenue_per_year(return_per_year_df)