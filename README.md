# scraping-drinks

Openrefine usage
./openrefine-batch.sh -a input/ -b config/ -c OUTPUT/ -f csv -m 512m -RX 

https://github.com/opencultureconsulting/openrefine-batch#usage

## install selnium stuff
pip3 install selenium

## install chromium driver
sudo apt-get install chromium-chromedriver


## Setting up crontabs
Run each scraper then reboot (the scripts were crashing without a reboot) then move the output files to /input
40 21 * * 2 cd /home/pi/scraping-drinks && /usr/bin/python3 Scrape_Obriens.py >> /home/pi/scraping-drinks/Log_Obriens.log 2>&1
55 21 * * 2 sudo shutdown -r
10 22 * * 2 cd /home/pi/scraping-drinks && /usr/bin/python3 Scrape_Supervalu.py >> /home/pi/scraping-drinks/Log_Supervalu.log 2>&1
25 22 * * 2 sudo shitdown -r
40 22 * * 2 cd /home/pi/scraping-drinks && /usr/bin/python3 Scrape_Tesco.py >> /home/pi/scraping-drinks/Log_Tesco.log 2>&1
55 22 * * 2 sudo shutdown -r
05 23 * * 2 cd /home/pi/scraping-drinks && mv 2020* /home/pi/scraping-drinks/other
