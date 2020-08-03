# import libraries
import urllib.request as urllib
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
from urllib.request import Request, urlopen

strip_previous_price = re.compile('(was)\s+\d+\.\d+', re.IGNORECASE)
stuff_heads=['Name','Price','Offer','PreviousPrice']
df = pd.DataFrame()
nao = 1
incrementor = 1

bases=['https://shop.supervalu.ie/shopping/wine-beer-spirits/c-150100075',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-vodka/c-150302430',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-irish-whiskey/c-150302435',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-american-whiskey/c-150302450',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-scotch-whisky/c-150302440',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-brandy/c-150302455',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-cream-liquers/c-150302460',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-gin/c-150302465',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-rum/c-150302475',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-other/c-150302480',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-lager/c-150302375',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-stout/c-150302380',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-ale/c-150302385',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-lager/c-150302386',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-stout/c-150302387',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-ale/c-150302388',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-cider/c-150302389',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-cider/c-150302390',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-alcopops/c-150302395',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-rose/c-150302555',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-other-fortified-dessert-wines/c-150410130',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-port/c-150410125',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-sherry/c-150410120',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-champagne-sparkling/c-150302545',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-australia/c-150409945',
'https://shop.supervalu.ie/shopping/wine-beer-spirits-chile/c-150409950']

for base in bases:
    while True:

        other = base + str('?page=') + str(4)   
        print(other)
        
        
        try:
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(other, headers=hdr)
            page = urlopen(req)
            soup = BeautifulSoup(page, "html.parser")  
        except:
            break
   
        data=[] 

        items = list(soup.find_all(class_=['ga-product']))            
            
        for item in items:
            product_name = item.find(class_="product-list-item-details-title")
            #print(product_name)
            try:
              product_name = product_name.get_text()
            except:
              product_name = ""
            price = item.find(class_="product-details-price-item")

            try:
              price = price.get_text().strip('Special Price\n\n€')  
            except:
              price = ""
            

            offer = item.find(class_="product-details-promotion-name")
            try:
                offer = offer.get_text().strip('\n')
                previous_price = strip_previous_price.search(offer)
                previous_price = previous_price.group().strip('Was WAS ')  
            except:
                previous_price = ""
                offer = ""       

            stuff = [product_name,price,offer,previous_price]
            data.append(stuff)
        
        df = df.append(data,ignore_index=True)
        #I found a hack so I wouldn't need to access each page by setting it to page 4,
        #each page had 25 items, and no single category page had more than 100 (so 4 pages)
        break


df.columns = stuff_heads

date_today = datetime.datetime.today().strftime('%Y%m-%W')
scraped_today = datetime.datetime.today().strftime('%Y%m%d')

df['Retailer'] = 'SuperValu'
df['DateScraped'] = scraped_today

df = df.drop_duplicates()

df.to_csv(date_today + '-SuperValu.csv', index=False)
