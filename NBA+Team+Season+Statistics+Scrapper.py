
# coding: utf-8

# In[84]:
from selenium import webdriver
import pandas as pd
import numpy as np
import time
import re
from collections import OrderedDict


# In[85]:

# start_year = str(2016)
# final_start = str(2000)
# final_end = str(int((final_start)[2:]) + 1)
# season = "{}-{}".format(start_year,end_year.zfill(2))
# final_season = "{}-{}".format(final_start,final_end.zfill(2))


# In[86]:

driver = webdriver.Chrome(executable_path="/Users/JiaJun/Downloads/chromedriver")


# In[87]:

filepath = "https://stats.nba.com/teams/boxscores-traditional/?Season=2016-17&SeasonType=Regular%20Season"
driver.get(filepath)


# In[76]:

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


# In[71]:

plyr = driver.find_elements_by_tag_name('tr')


# In[72]:

file = []
for row in plyr:
    file.append(row.text)
file = file[:31]


# In[73]:

dic = OrderedDict()
for i in file[0].split(" "):
    dic[i] = []
dic['Season'] = []


# In[78]:

button = driver.find_element_by_xpath(r"//div[@class='stats-table-pagination__inner stats-table-pagination__inner--top']//div[@class='stats-table-pagination__info']//a[@class='stats-table-pagination__next']")
while True:
    plyr = driver.find_elements_by_tag_name('tr')
    dic = func(plyr)
    button.click()
    time.sleep(3)


# In[80]:

df = pd.DataFrame(dic)


# In[81]:

df.to_csv(r"/Users/JiaJun/Desktop/Jupyter Notebook/nba-teams.csv",index=None)

