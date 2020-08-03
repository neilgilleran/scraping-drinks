#!/usr/bin/env python
# coding: utf-8

"""
{Desc} This script will scrape data from OBriens
[Author] Neil Gilleran
"""


# import libraries
#import urllib.request as urllib
import urllib.request
#import urllib


# set options to be headless, ..
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import requests


#Can expand this to include the link href and img src in future
#stuff_heads=['Name','Price','Special Price','Old Price','Offer','Link']
stuff_heads=['Name','Price','SpecialPrice','PreviousPrice','Offer']
df = pd.DataFrame()
nao = 1
incrementor = 1
bases=['https://www.obrienswine.ie/collections/spirits?page=',
        'https://www.obrienswine.ie/collections/wine?page=',
        'https://www.obrienswine.ie/collections/beer?page=',
        'https://www.obrienswine.ie/collections/champange-sparkling?page=',
        'https://www.obrienswine.ie/collections/mixed-cases?page=',
        'https://www.obrienswine.ie/collections/gifts?page=']

hdr = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0' }

try:
	wd = webdriver.Chrome('chromedriver',options=options)
	print("driver loaded!")
except:
	print("driver did not laod")

for base in bases:
    #print(base)
    while True:
   
        #enabling this here for testing
        #base = 'https://www.obrienswine.ie/collections/wine?page='
        #print(base)

        other = base + str(nao)
        print(other)
        

        """ Selenium method"""
        wd.get(other)
        page = wd.page_source

        soup = BeautifulSoup(page, 'html.parser')
  
        data=[] 
        
        items = soup.find_all(class_=['ais-Hits-item'])
        
        print(len(items))
        if len(items) == 0:
            nao = 1
            break

        for item in items:

            product_name = item.find(class_="product-title")
            try:
                product_name = product_name.get_text()
            except:
                product_name = "" 

            price = item.find(class_="product-price")
            try:
                price = price.get_text().strip('\nRegular Special Price\n\n     €')  
            except:
                price = ""

            special_price = item.find(class_="product-discounted")
            try:
                special_price = special_price.get_text().strip('\nSpecial Price\n\n     €')  
            except:
                special_price = ""

            old_price = item.find(class_="product-compare")
            try:
                old_price = old_price.get_text().strip('\nSpecial Price\n\n     € Regular Price:\n\n                    ')  
            except:
                old_price = ""

            offer = item.find(class_="product-offer")
            try:
                offer = offer.get_text()
            except:
                offer = ""
                
            #link = item.find(class_="product-card-image", href=True)
            #try:
            #    link = link.get('href')
            #except:
            #    print("it has to have a link")
            
            country = item.find(class_="product-additional")
            try:
                country = country.get_text().strip('\xa0\n')
            except:
                country = ""
                

            #stuff=['Name','Price','Special Price','Old Price','Offer']
            stuff = [product_name,price,special_price,old_price,offer]
            data.append(stuff)
        df = df.append(data,ignore_index=True)

        nao = incrementor + nao


df.columns = stuff_heads
df.describe()


#Merge the two of these, this is bad, I need to update this later
df['Price'] = df['Price'].map(str) + df['SpecialPrice']

df = df.drop('SpecialPrice',axis=1)


date_today = datetime.datetime.today().strftime('%Y%m-%W')
print(date_today)
scraped_today = datetime.datetime.today().strftime('%Y%m%d')

df['Retailer'] = 'OBriens'
df['DateScraped'] = scraped_today

#remove duplicates
df = df.drop_duplicates()

#Export the name of the file as YYYYMM-WW (Year,Month,WeekNumber)
try:
    df.to_csv(date_today + '-obriens.csv', index=False)
    print("outputting file")
except:
    print("problem wirting the file")

