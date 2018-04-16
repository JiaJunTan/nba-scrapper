# Importing required libraries
from selenium import webdriver
from bs4 import BeautifulSoup as bsoup
from collections import OrderedDict
import pandas as pd
import numpy as np

# Defining season of interest to scrap
start_year = str(2016)
end_year = str(int(start_year)+1)[2:].zfill(2)
season = "{}-{}".format(start_year,end_year)

# Selenium's WebDriver for webpage automation and BeautifulSoup as parser
driver = webdriver.Chrome(executable_path="/Users/JiaJun/Downloads/chromedriver")
filepath = "https://stats.nba.com/teams/boxscores-traditional/?Season={}&SeasonType=Regular%20Season".format(season)
driver.get(filepath)
bs_obj = bsoup(driver.page_source, 'html.parser')
rows = bs_obj.find_all('table')[0].find_all('tr')

# OrderedDictionary to store scrapped data and defining keys as DataFrame columns
file = []
for row in rows:
    file.append(row.get_text().strip().split("\n"))

dic = OrderedDict()
for i in file[0]:
    if i == 'Match\xa0Up':
        dic['Match'] = []
    elif i == 'Game\xa0Date':
        dic['Date'] = []
    else:
        dic[i] = []
        
# Main function in loop to process and store data
def func(rows):
    file2 = []
    for row in rows:
        file2.append(row.get_text().strip().split("\n"))
    file2 = np.transpose(file2[1:])
    i = 0
    for key in dic.keys():
        dic[key].extend(list(file2[i]))
        i += 1
    return dic

# Automation through WebDriver and looping through all pages of data 
button = driver.find_element_by_xpath(r"//div[@class='stats-table-pagination__inner stats-table-pagination__inner--top']//div[@class='stats-table-pagination__info']//a[@class='stats-table-pagination__next']")
page = 1
while page <= 50:
    bs_obj = bsoup(driver.page_source, 'html.parser')
    rows = bs_obj.find_all('table')[0].find_all('tr')
    dic = func(rows)
    button.click()
    page += 1

# Transforming into DataFrame and exporting as csv
df = pd.DataFrame(dic)
filedestination = r"/Users/JiaJun/Desktop/nba-teams_{}.csv".format(season)
df.to_csv(filedestination,index=None)
