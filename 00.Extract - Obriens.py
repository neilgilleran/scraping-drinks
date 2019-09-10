#!/usr/bin/env python
# coding: utf-8

"""
{Desc} This script will scrape data from OBriens
[Author] Neil Gilleran
"""


# import libraries
import urllib.request as urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np
import datetime


#Can expand this to include the link href and img src in future
#stuff_heads=['Name','Price','Special Price','Old Price','Offer','Link']
stuff_heads=['Name','Price','SpecialPrice','PreviousPrice','Offer']
df = pd.DataFrame()
nao = 1
incrementor = 1
bases=['https://www.obrienswine.ie/spirits/page/',
        'https://www.obrienswine.ie/wine/page/',
      'https://www.obrienswine.ie/beers/page/',
      'https://www.obrienswine.ie/gifts-accessories/page/']
for base in bases:
    #print(base)
    while True:
   
    #base = 'https://www.obrienswine.ie/wine/page/'

        other = base + str(nao) + str('.html')
        #print(other)

        try:
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(other, headers=hdr)
            page = urlopen(req)
            soup = BeautifulSoup(page, "lxml")
        except:
            break

    
        """
        We needed a way to catch 'Items 1 to 30 of 750 total'
        """
        total_items = soup.find(class_="amount")
        total_items = total_items.get_text()
        print(total_items)
        p = re.compile('of\s\d+')
        x = re.search(p,total_items)
        #this code is a limitter to break out of the loop, it threw an error when it couldnt find another
        try:
            y = x.group()
            y = int(y.strip('of '))  
        except:
            print("There was no limit set for y")
            
        data=[] 
        #items = soup.findAll("li", {"class" : lambda L: L and L.startswith('product-list--list-item')})
        items = list(soup.find_all(class_="item"))
        #print(len(items))


        for item in items:

            product_name = item.find(class_="product-name")
            try:
                product_name = product_name.get_text()
            except:
                product_name = "" 

            price = item.find(class_="regular-price")
            try:
                price = price.get_text().strip('\nRegular Special Price\n\n     €')  
            except:
                price = ""

            special_price = item.find(class_="special-price")
            try:
                special_price = special_price.get_text().strip('\nSpecial Price\n\n     €')  
            except:
                special_price = ""

            old_price = item.find(class_="old-price")
            try:
                old_price = old_price.get_text().strip('\nSpecial Price\n\n     € Regular Price:\n\n                    ')  
            except:
                old_price = ""

            offer = item.find(class_="custom-onsale-category-label-text")
            try:
                offer = offer.get_text()
            except:
                offer = ""
                
            link = item.find(class_="product-image", href=True)
            try:
                link = link.get('href')
            except:
                print("it has to have a link")
            
            country = item.find(class_="product-location")
            try:
                country = country.get_text().strip('\xa0\n')
            except:
                country = ""
                

            #stuff=['Name','Price','Special Price','Old Price','Offer']
            stuff = [product_name,price,special_price,old_price,offer]
            data.append(stuff)
        df = df.append(data,ignore_index=True)

        #this needs to be after because the website will allow page=n where n is any value (ie it will keep
        #on incrementing)
        if len(items) < 30:
            #print("Break when here?")
            nao = 1
            break
        
        #this is to break the loop if the number of items are evenly divided by 30
        try:
            if y/30 == nao:
              #print("Page limit reached so break")
              break 
        except:
            print("Might be a problem with the y limiter")    
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

