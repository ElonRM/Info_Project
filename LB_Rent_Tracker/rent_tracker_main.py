import csv
from time import sleep
from selenium import webdriver
import pandas as pd

driver = webdriver.Chrome("/Users/timehmann/Documents/Programmieren/VSCode/Python/Add-Ons/Chromedriver/chromedriver")
driver.get("https://app.lootbear.com/")
#driver.get("https://youtube.com")

def get_new_data():
    i = 1
    start = False
    while start == False:
        try:
            id_element = driver.find_element_by_xpath("""//*[@id="app"]/div[1]/div/div/div/div/div[2]/div/div[5]/div/div/div/div[1]/div/table/tbody/tr[1]/td[1]""")
            id = id_element.text
            start = True
            print("start")
        except: pass

    rent_revenue_data = [['0', '0', '0', '0']]

    df = pd.DataFrame(rent_revenue_data)
    df.columns = ['ID', 'Date', 'Item', 'Revenue']
    df.to_csv('rent_revenue_data.csv')

    while 1:
        try:
            #driver.find_element_by_xpath("//*[@id=\"app\"]/div[1]/div/button").click()
            #driver.find_element_by_xpath("//*[@id=\"logo-icon\"]").click()
            id = driver.find_element_by_xpath(f"//*[@id=\"app\"]/div[1]/div/div/div/div/div[2]/div/div[5]/div/div/div/div[1]/div/table/tbody/tr[{i}]/td[1]").text
            #id = id_element.text
            date = driver.find_element_by_xpath(f"//*[@id=\"app\"]/div[1]/div/div/div/div/div[2]/div/div[5]/div/div/div/div[1]/div/table/tbody/tr[{i}]/td[2]").text
            item = driver.find_element_by_xpath(f"//*[@id=\"app\"]/div[1]/div/div/div/div/div[2]/div/div[5]/div/div/div/div[1]/div/table/tbody/tr[{i}]/td[3]").text
            revenue = driver.find_element_by_xpath(f"//*[@id=\"app\"]/div[1]/div/div/div/div/div[2]/div/div[5]/div/div/div/div[1]/div/table/tbody/tr[{i}]/td[4]").text.strip("$")
            new_data = [id, date, item, revenue]
            print(new_data)
            rent_revenue_data.append(new_data)
            with open('rent_revenue_data.csv', 'a') as f: 
                write = csv.writer(f) 
                write.writerow(new_data)

            if i%5 == 0:
                driver.find_element_by_xpath("""//*[@id="app"]/div[1]/div/div/div/div/div[2]/div/div[5]/div/div/div/div[2]/div""").click()
            i += 1
        except Exception as e:
            sleep(1)
            #print(e)

def update_data():
    """ Updates the list of revenue data"""
    
    #gets the id of the old newest revenue entry
    with open('rent_revenue_data.csv', 'r') as file:
        reader = list(csv.reader(file))
        newest_data_id = reader[1][0]
        print(newest_data_id)
    
    i = 1
    '''start = False
    while start == False:
        try:
            id_element = driver.find_element_by_xpath("""//*[@id="app"]/div[1]/div/div/div/div/div[2]/div/div[5]/div/div/div/div[1]/div/table/tbody/tr[1]/td[1]""")
            id = id_element.text
            start = True
            print("start")
        except: pass'''
    
    while 1:
        try:
            #driver.find_element_by_xpath("//*[@id=\"app\"]/div[1]/div/button").click()
            #driver.find_element_by_xpath("//*[@id=\"logo-icon\"]").click()
            id = driver.find_element_by_xpath(f"//*[@id=\"app\"]/div[1]/div/div/div/div/div[2]/div/div[5]/div/div/div/div[1]/div/table/tbody/tr[{i}]/td[1]").text
            if id == newest_data_id: break
            #id = id_element.text
            date = driver.find_element_by_xpath(f"//*[@id=\"app\"]/div[1]/div/div/div/div/div[2]/div/div[5]/div/div/div/div[1]/div/table/tbody/tr[{i}]/td[2]").text
            item = driver.find_element_by_xpath(f"//*[@id=\"app\"]/div[1]/div/div/div/div/div[2]/div/div[5]/div/div/div/div[1]/div/table/tbody/tr[{i}]/td[3]").text
            revenue = driver.find_element_by_xpath(f"//*[@id=\"app\"]/div[1]/div/div/div/div/div[2]/div/div[5]/div/div/div/div[1]/div/table/tbody/tr[{i}]/td[4]").text.strip("$")
            new_data = [id, date, item, revenue]
            print(new_data)

            with open('rent_revenue_data.csv', 'r') as file:
                reader = list(csv.reader(file))
                reader.insert(i, new_data)

            with open('rent_revenue_data.csv', 'w') as update:
                writer = csv.writer(update)
                for line in reader:
                    writer.writerow(line)

            if i%5 == 0:
                driver.find_element_by_xpath("""//*[@id="app"]/div[1]/div/div/div/div/div[2]/div/div[5]/div/div/div/div[2]/div""").click()
            i += 1
        except Exception as e:
            sleep(1)
            print(e)

    ''' with open('test_csv.csv', 'a') as update:
        writer = csv.writer(update)
        for line in reader:
            writer.writerow(line)'''
update_data()
