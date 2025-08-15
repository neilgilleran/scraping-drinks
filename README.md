# scraping-drinks

Openrefine usage
./openrefine-batch.sh -a input/ -b config/ -c OUTPUT/ -f csv -m 512m -RX

https://github.com/opencultureconsulting/openrefine-batch#usage

## install selenium stuff
pip3 install selenium

## install chromium driver
sudo apt-get install chromium-chromedriver

## Running scrapers
The individual retailer scripts have been combined into `scraper.py`. Configuration for each retailer lives in `config/retailers.json`.

Run all scrapers:
```
python scraper.py
```

## Setting up crontabs
Run the scraper then reboot (the scripts were crashing without a reboot) then move the output files to /input
```
40 21 * * 2 cd /home/pi/scraping-drinks && /usr/bin/python3 scraper.py >> /home/pi/scraping-drinks/scraper.log 2>&1
55 21 * * 2 sudo shutdown -r
05 23 * * 2 cd /home/pi/scraping-drinks && mv 2020* /home/pi/scraping-drinks/other
```
