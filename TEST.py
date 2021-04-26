#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from webdrivermanager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import matplotlib.ticker as ticker
from urllib.request import urlopen
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
import seaborn as sns
import pandas as pd
import numpy as np
import selenium
import requests
import unittest
import time
import re
import sys


# In[2]:


def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height

def all_links(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    # Setup the driver. This one uses chrome with some options and a path to the chromedriver
    driver = webdriver.Chrome(executable_path='C:\Program Files\chromedriver.exe')
    # implicitly_wait tells the driver to wait before throwing an exception
    driver.implicitly_wait(5)
    # driver.get(url) opens the page
    driver.get('https://collegedunia.com/germany-colleges')
    # This starts the scrolling by passing the driver and a timeout
    scroll(driver, 5)
    # Once scroll returns bs4 parsers the page_source
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # Them we close the driver as soup_a is storing the page source
    driver.close()
    
    alls = []
    
    for d in soup.findAll('div', attrs={'class':'jsx-1879893061 listing-block text-uppercase bg-white position-relative'}):

                name = d.find('h3', attrs={'class':'jsx-1879893061 text-white font-weight-bold text-md m-0'})
                location = d.find('span', attrs={'class':'jsx-1879893061 mr-1'})
                rating = d.find('span', attrs={'class':'jsx-1879893061 rating-text text-white font-weight-bold text-base d-block text-right'})
                scores = d.find('span', attrs={'class':'jsx-1879893061 d-block'})
                price = d.find('span', attrs={'class':'jsx-1879893061 d-flex justify-content-between'})

                all1=[]

                if name is not None:
                    #print(n[0]['alt'])
                    all1.append(name.text)
                else:
                    all1.append("N/A")

                if location is not None:
                    all1.append(location.text)
                else:    
                    all1.append('N/A')

                if rating is not None:
                    #print(rating.text)
                    all1.append(rating.text)
                else:
                    all1.append('N/A')

                if scores is not None:
                    #print(price.text)
                    all1.append(scores.text)
                else:
                    all1.append('N/A')     

                if price is not None:
                    #print(price.text)
                    all1.append(price.text)
                else:
                    all1.append('N/A')
                alls.append(all1)    
    return alls


# In[3]:


results = []
for i in range(1):
    results.append(all_links(i))
flatten = lambda l: [item for sublist in l for item in sublist]
df = pd.DataFrame(flatten(results),columns=['UNIVERSITY NAME','LOCATION','RATING','SCORES','PRICE'])

#cleaning data for ML and Data Engineering. 

df["UNIVERSITY NAME"] = df["UNIVERSITY NAME"].str.replace(',', '')
df['UNIVERSITY NAME'] = pd.to_numeric(df['UNIVERSITY NAME'], errors='ignore')

df["LOCATION"] = df["LOCATION"].str.replace(',', '')
df["LOCATION"] = df["LOCATION"].str.replace('germany', '')

df['RATING'] = df['RATING'].str.replace('/', '')
df['RATING'] = df['RATING'].str.replace('10', '')

df['PRICE'] = df['PRICE'].str.extract('([0-9][,.]*[0-9]*)')
#df['PRICE'] = df['PRICE'].apply(lambda x: find_number(x))

df[['GREGMAT','IELTSTOEFL']] = df.SCORES.str.split("|",expand=True)

df.to_csv('germany.csv', index=False, encoding='utf-8')


# In[4]:


df = pd.read_csv("germany.csv")
df.shape


# In[14]:


df.head(10)


# In[6]:


df.dtypes


# In[23]:


data = df.sort_values(["RATING"], axis=0, ascending=False)[:75]
data


# In[24]:


from bokeh.models import ColumnDataSource
from bokeh.transform import dodge
import math
from bokeh.io import curdoc
curdoc().clear()
from bokeh.io import push_notebook, show, output_notebook
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.models import Legend
output_notebook()


# In[25]:


p = figure(x_range=data.iloc[:,0], plot_width=800, plot_height=550, title="Authors Highest Priced Book", toolbar_location=None, tools="")

p.vbar(x=data.iloc[:,0], top=data.iloc[:,2], width=0.9)

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.major_label_orientation = math.pi/2


# In[26]:


show(p)


# In[27]:


data = df.sort_values(["PRICE"], axis=0, ascending=False)[:75]
data


# In[28]:


p = figure(x_range=data.iloc[:,0], plot_width=800, plot_height=550, title="Authors Highest Priced Book", toolbar_location=None, tools="")

p.vbar(x=data.iloc[:,0], top=data.iloc[:,4], width=0.9)
p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.major_label_orientation = math.pi/2


# In[29]:


show(p)


# In[ ]:




