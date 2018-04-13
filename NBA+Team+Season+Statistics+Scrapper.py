from selenium import webdriver
import pandas as pd
import numpy as np
import time
import re
from collections import OrderedDict

driver = webdriver.Chrome(executable_path="/Users/JiaJun/Downloads/chromedriver")

start_year = str(2016)
end_year = str(int(start_year)+1)[2:].zfill(2)
season = "{}-{}".format(start_year,end_year)

filepath = "https://stats.nba.com/teams/boxscores-traditional/?Season={}&SeasonType=Regular%20Season".format(season)
driver.get(filepath)

def func(plyr_copy):
    file2 = []
    for row in plyr:
        file2.append(row.text)
        file2 = file2[:31]
    dic['TEAM'].extend(list(map(lambda x: x.split("\n")[1] ,file2[1:])))
    remaining_data = list(np.transpose(list(map(lambda x: x.split("\n")[2].split(" ") ,file2[1:]))))
    i = 0
    for col in list(dic.keys())[1:-1]:
        dic[col].extend(remaining_data[i])
        i += 1
    dic['Season'].extend([season]*30)
    print(season)
    return dic

plyr = driver.find_elements_by_tag_name('tr')

file = []
for row in plyr:
    file.append(row.text)
file = file[:31]

dic = OrderedDict()
for i in file[0].split(" "):
    dic[i] = []
dic['Season'] = []

button = driver.find_element_by_xpath(r"//div[@class='stats-table-pagination__inner stats-table-pagination__inner--top']//div[@class='stats-table-pagination__info']//a[@class='stats-table-pagination__next']")
while True:
    plyr = driver.find_elements_by_tag_name('tr')
    dic = func(plyr)
    button.click()
    time.sleep(3)

df = pd.DataFrame(dic)

df.to_csv(r"/Users/JiaJun/Desktop/Jupyter Notebook/nba-teams.csv",index=None)
