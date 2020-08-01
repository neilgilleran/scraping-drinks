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

stuff_heads=['Name','Price','PreviousPrice','Offer']
strip_previous_price = re.compile('(was)\s+\d+\.\d+', re.IGNORECASE)
#df = pd.DataFrame()
df = pd.DataFrame(pd.np.empty((0, 4)))    
nao = 0
incrementor = 20
bases=['https://www.tesco.ie/groceries/product/browse/default.aspx?N=4294531818&Ne=4294954028&Nao=',
'https://www.tesco.ie/groceries/product/browse/default.aspx?N=4294794608&Ne=4294954028&Nao=',
'https://www.tesco.ie/groceries/product/browse/default.aspx?N=4294953032&Ne=4294954028&Nao=']


hdr = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0' }

wd = webdriver.Chrome('chromedriver',options=options)


for base in bases:

    while True:

        other = base + str(nao)
        print(other)
      

        """ Selenium method"""
        wd.get(other)
        page = wd.page_source
        
        
        soup = BeautifulSoup(page, 'html.parser')
              
     
        data=[] 
        items = soup.findAll("li", {"id" : re.compile('p-.*')})
        #items = soup.findAll("li")

        if len(items) < 1:
            nao = 0
            #print(items)
            print("Didnt find any items so breaking")
            break
        else:
            for item in items:
                product_name = item.find(class_="inBasketInfoContainer")
                try:
                  product_name = product_name.get_text()
                except:
                  product_name = ""


                price = item.find(class_="linePrice")
                try:
                  price = price.get_text().strip('Special Price\n\n€')  
                except:
                  price = ""

                offer = item.find(class_="promoFlyout")
                try:
                    offer = offer.get_text()
                except:
                    offer = ""

                previous = item.find(class_="promoFlyout")
                try:
                    previous = previous.get_text()
                    previous = strip_previous_price.search(previous)
                    previous = previous.group().strip('Was WAS ')
                except:
                    previous = ""

                stuff = [product_name,price,previous,offer]
                data.append(stuff)
                print(data)
        df = df.append(data,ignore_index=True)
        
        nao = incrementor + nao


df.columns = stuff_heads


try:
    date_today = datetime.datetime.today().strftime('%Y%m-%W')
except:
    print("issue here")

scraped_today = datetime.datetime.today().strftime('%Y%m%d')

df['Retailer'] = 'Tesco - IRL'
df['DateScraped'] = scraped_today

#remove duplicates
df = df.drop_duplicates()

df.to_csv(date_today + '-Tesco.csv', index=False)