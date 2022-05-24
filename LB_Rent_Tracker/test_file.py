import pandas as pd
from pprint import pprint
"""
test_lst = [['15826354', '26/3/2022 9:46 AM', '★ Karambit | Scorched (Minimal Wear)', '$0.27']]
test_lst.append(['15827543', '26/3/2022 2:49 PM', '★ Talon Knife | Stained (Minimal Wear)', '$0.28'])
df = pd.DataFrame(test_lst)
df.columns = ['ID', 'Date', 'Item', 'Revenue']
df.to_csv('rent_revenue_data.csv')



import csv

with open('rent_revenue_data.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

items = []
print(data)
for pay_out in data:
    if pay_out[2] not in items:
        items.append(pay_out[2])

print(items, len(items))

d1 = "01/08/2021 10:12 AM".split(" ")[0]
print(d1)


td = {}

td["hello"] = "helo"
td["servus"] = {"moin": "tach"}

print(td)
print(td["servus"]["moin"])

from data_analysis import *

plt.plot(xs, ys)
plt.show()


dt = {}
lst = ['a','b','c','d','e','f','g']

for number, letter in enumerate(lst):
    try:
        dt[letter]["test"] += number
    except:
        dt[letter] = {"test": number}

for number, letter in enumerate(lst):
    try:
        dt[letter]["test"] += number
    except:
        dt[letter] = {"test": number}

print(dt)"""

import csv

with open('test_csv.csv', 'a') as file:
    reader = list(csv.reader(file))
    reader.insert(1, [1,2,3,4])

with open('test_csv.csv', 'a') as update:
    writer = csv.writer(update)
    for line in reader:
        writer.writerow(line)
