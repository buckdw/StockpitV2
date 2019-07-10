# stockpit requisites

mysql -user root --password=j0sepace
create catalog Stockpit

## general requisites
sudo pip install mysql-connector-python

## stocks requisites
sudo pip install yfinance -U

## stockinfo requisites 
sudo pip install yahoo_fin
sudo pip install requests_html
sudo pip install html5lib

## execution
python stocks.py --file stock.txt
python stockinfo.py -- file stock.txt

beiden gebruiken stock.txt als invoer bestand
