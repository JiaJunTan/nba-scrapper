# Importing libraries
from selenium import webdriver
from bs4 import BeautifulSoup as bsoup
import pandas as pd
import numpy as np
import re
from collections import OrderedDict

# Establishing seasons to scrap
start_year = str(2008)
end_year = str(int(start_year)+1)[2:].zfill(2)
season = "{}-{}".format(start_year,end_year)
season

# Selenium automated browser
weblink = 'http://stats.nba.com/players/boxscores/?Season={}&SeasonType=Regular%20Season'.format(season)
driver = webdriver.Chrome(executable_path="/Users/JiaJun/Downloads/chromedriver") 
driver.get(weblink)

# Main function 
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


# Parsing using BeautifulSoup
bs_obj = bsoup(driver.page_source, 'html.parser')
rows = bs_obj.find_all('table')[0].find_all('tr')


# Dictionary to store data & keys to include
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

# Total pages (tables) to scroll through 
total_pages = driver.find_element_by_xpath(r"//div[@class='stats-table-pagination__inner stats-table-pagination__inner--top']")
total_pages = int(re.findall(r"of (\d+)",total_pages.text)[0])


# Automating scrolling of tables, and cleaning data to store in dictionary
button = driver.find_element_by_xpath(r"//div[@class=\'stats-table-pagination__inner stats-table-pagination__inner--top\']//div[@class=\'stats-table-pagination__info\']//a[@class=\'stats-table-pagination__next\']")

page = 1 
while page <= total_pages:
	bs_obj = bsoup(driver.page_source, 'html.parser')
	rows = bs_obj.find_all('table')[0].find_all('tr')
	dic = func(rows)
	button.click()
	page += 1

# Converting to dataframe and exporting as CSV 
df = pd.DataFrame(dic)
df['season'] = [season]*df.shape[0]

filedestination = r"/Users/JiaJun/Desktop/nba-players_{}.csv".format(season) # change filepath here 

df.to_csv(filedestination,index=None)





