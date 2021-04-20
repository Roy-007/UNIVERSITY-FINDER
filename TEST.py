#!/usr/bin/env python
# coding: utf-8

# In[22]:


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


# In[23]:


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
    driver.implicitly_wait(100)
    # driver.get(url) opens the page
    driver.get('https://collegedunia.com/germany-colleges')
    # This starts the scrolling by passing the driver and a timeout
    scroll(driver, 180)
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
                    all1.append('-*-')     

                if price is not None:
                    #print(price.text)
                    all1.append(price.text)
                else:
                    all1.append('-*-')
                alls.append(all1)    
    return alls


# In[24]:


results = []
for i in range(1):
    results.append(all_links(i))
flatten = lambda l: [item for sublist in l for item in sublist]
df = pd.DataFrame(flatten(results),columns=['UNIVERSITY NAME','LOCATION','RATING','SCORES','PRICE'])
df.to_csv('germany.csv', index=False, encoding='utf-8')


# In[25]:


df = pd.read_csv("germany.csv")
df.shape


# In[26]:


df.head(50)


# In[ ]:




