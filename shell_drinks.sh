TIMESTAMP=`date "+%Y-%m-%d-%H:%M:%S"`

echo $TIMESTAMP

touch script_started-$TIMESTAMP.tmp


python3 Scrape_Supervalu.py
sleep 10
python3 Scrape_Tesco.py
sleep 10
python3 Scrape_Obriens.py

touch script_ended-$TIMESTAMP.tmp

