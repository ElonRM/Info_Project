import csv
from pprint import pprint
from datetime import datetime
import matplotlib.pyplot as plt

with open('rent_revenue_data.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

# entfernen der Kopfzeile
### [ID, DATE, ITEM, REVENUE]
data.pop(0)

# in rent_dict wird ein Dictionary erstellt, welches für jeden Skin (key) eine Liste
# der Renevue Entries beinhaltet (tuple aus tag und betrag)
rent_dict = {}
for revenue_entry in data:
    try:
        rent_dict[revenue_entry[2]] = rent_dict[revenue_entry[2]] + [(revenue_entry[1], revenue_entry[3])]
    except Exception as e:
        print(e)
        rent_dict[revenue_entry[2]] = [(revenue_entry[1], revenue_entry[3])]

# revenue_by_skin ist eine Liste für die summierte Einnahme pro Skin
revenue_by_skin=[(name, round(sum(float(entry[1]) for entry in val), 2)) for val, name in zip(rent_dict.values(), rent_dict.keys())]
revenue_by_skin.sort(key = lambda tup: tup[1], reverse = True)
#pprint(revenue_by_skin)


def datediff(d1, d2):
    """gibt die Differenz zwischen 2 Tagen zurück"""

    d1 = datetime.strptime(d1, "%d/%m/%Y")
    d2 = datetime.strptime(d2, "%d/%m/%Y")
    return abs((d2-d1).days)

# cumulated_revenue_by_rent_time ist ein Dictionary, welches für jeden Skin
# eine Liste bestehend aus der bis zu einem Vermietungseintrag Gesamteinnahmen und 
# den Vergangen Tagen beinhaltet
cumulated_revenue_by_rent_time={}
for val, name in zip(rent_dict.values(), rent_dict.keys()):
    for entry in reversed(val):
        try:
            cumulated_revenue_by_rent_time[name]["revenue_history"] = cumulated_revenue_by_rent_time[name]["revenue_history"] + [(datediff(cumulated_revenue_by_rent_time[name]["start"], entry[0].split(" ")[0]), round(cumulated_revenue_by_rent_time[name]["revenue_history"][-1][-1] + float(entry[1]), 2))]
        except Exception as e:
            print(e)
            cumulated_revenue_by_rent_time[name] = {"start": entry[0].split(" ")[0], "revenue_history":[(0,round(float(entry[1]), 2))]}

cumulated_revenue_by_rent_time_from_first={}
for val, name in zip(rent_dict.values(), rent_dict.keys()):
    # schneidet somit die ältesten 7 Items ab, da nach diesen über 7 Monate nichts kommt
    # Somit wird das Diagramm sehr viel übersichtlicher.
    if name == "MP7 | Fade (Factory New)":
        break
    for entry in reversed(val):
        try:
            cumulated_revenue_by_rent_time_from_first[name]["revenue_history"] = cumulated_revenue_by_rent_time_from_first[name]["revenue_history"] + [(datediff("18/01/2021", entry[0].split(" ")[0]), round(cumulated_revenue_by_rent_time_from_first[name]["revenue_history"][-1][-1] + float(entry[1]), 2))]
        except Exception as e:
            print(e)
            cumulated_revenue_by_rent_time_from_first[name] = {"start": entry[0].split(" ")[0], "revenue_history":[(datediff("18/01/2021", entry[0].split(" ")[0]),round(float(entry[1]), 2))]}

#print(cumulated_revenue_by_rent_time["★ Karambit | Autotronic (Field-Tested)"])

xs = [x for x,_ in cumulated_revenue_by_rent_time["★ Karambit | Autotronic (Field-Tested)"]["revenue_history"]]
ys = [y for _,y in cumulated_revenue_by_rent_time["★ Karambit | Autotronic (Field-Tested)"]["revenue_history"]]

if __name__ == "__main__":
    #plt.plot(xs, ys)
    #plt.show()
    pprint(revenue_by_skin)
    print(rent_dict.keys())
    for item in cumulated_revenue_by_rent_time_from_first.values():
        print(item)
        pass