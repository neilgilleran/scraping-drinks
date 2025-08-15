import json
import datetime
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


def parse_tesco(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    items = soup.find_all("li", {"id": re.compile('p-.*')})
    strip_previous = re.compile('(was)\\s+\\d+\\.\\d+', re.IGNORECASE)
    for item in items:
        name = item.find(class_="inBasketInfoContainer")
        name = name.get_text() if name else ""
        price = item.find(class_="linePrice")
        price = price.get_text().strip('Special Price\\n\\n€') if price else ""
        offer_el = item.find(class_="promoFlyout")
        offer = offer_el.get_text() if offer_el else ""
        previous = ""
        if offer:
            match = strip_previous.search(offer)
            previous = match.group().strip('Was WAS ') if match else ""
        data.append([name, price, previous, offer])
    return data


def parse_obriens(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    items = soup.find_all(class_=['ais-Hits-item'])
    for item in items:
        name = item.find(class_="product-title")
        name = name.get_text() if name else ""
        price = item.find(class_="product-price")
        price = price.get_text().strip('\\nRegular Special Price\\n\\n     €') if price else ""
        special = item.find(class_="product-discounted")
        special = special.get_text().strip('\\nSpecial Price\\n\\n     €') if special else ""
        old_price = item.find(class_="product-compare")
        old_price = old_price.get_text().strip('\\nSpecial Price\\n\\n     € Regular Price:\\n\\n                    ') if old_price else ""
        offer = item.find(class_="product-offer")
        offer = offer.get_text() if offer else ""
        final_price = special or price
        data.append([name, final_price, old_price, offer])
    return data


def parse_supervalu(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    strip_previous = re.compile('(was)\\s+\\d+\\.\\d+', re.IGNORECASE)
    items = list(soup.find_all(class_=['ga-product']))
    for item in items:
        name = item.find(class_="product-list-item-details-title")
        name = name.get_text() if name else ""
        price = item.find(class_="product-details-price-item")
        price = price.get_text().strip('Special Price\\n\\n€') if price else ""
        offer_el = item.find(class_="product-details-promotion-name")
        offer = offer_el.get_text().strip('\\n') if offer_el else ""
        previous = ""
        if offer:
            match = strip_previous.search(offer)
            previous = match.group().strip('Was WAS ') if match else ""
        data.append([name, price, previous, offer])
    return data


PARSERS = {
    'tesco': parse_tesco,
    'obriens': parse_obriens,
    'supervalu': parse_supervalu,
}


class RetailScraper:
    def __init__(self, config):
        self.name = config['name']
        self.bases = config['bases']
        self.increment = config.get('increment', 1)
        self.start = config.get('start', 0)
        self.use_selenium = config.get('use_selenium', False)
        self.page_param = config.get('page_param')
        self.max_page = config.get('max_page')
        self.parser = PARSERS[config['parser']]
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        if self.use_selenium:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome('chromedriver', options=options)
        else:
            self.driver = None

    def fetch_page(self, url):
        if self.use_selenium:
            self.driver.get(url)
            return self.driver.page_source
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def scrape(self):
        df = pd.DataFrame(columns=['Name', 'Price', 'PreviousPrice', 'Offer'])
        for base in self.bases:
            page = self.start
            while True:
                if self.page_param:
                    url = f"{base}{self.page_param}{page}"
                else:
                    url = base if page == 0 and not self.page_param else f"{base}{page}"
                html = self.fetch_page(url)
                data = self.parser(html)
                if not data:
                    break
                df = df.append(data, ignore_index=True)
                if self.max_page and page >= self.max_page:
                    break
                page += self.increment
        scraped_today = datetime.datetime.today().strftime('%Y%m%d')
        df['Retailer'] = self.name
        df['DateScraped'] = scraped_today
        df = df.drop_duplicates()
        date_today = datetime.datetime.today().strftime('%Y%m-%W')
        df.to_csv(f"{date_today}-{self.name}.csv", index=False)
        return df


def main():
    with open('config/retailers.json') as f:
        configs = json.load(f)
    for conf in configs:
        scraper = RetailScraper(conf)
        scraper.scrape()


if __name__ == '__main__':
    main()
