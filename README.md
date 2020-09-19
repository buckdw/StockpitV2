# stockpit requisites

mysql -user root --password=Emers0nFitti
create catalog stockpit

## general requisites
sudo pip install mysql-connector-python

## stocks requisites
sudo pip3 install lxml
sudo pip3 install yfinance -U
sudo pip3 install regex
/Application/Python3.8/Install.certificates


## execution
python stocks.py --file stock.txt
python stockinfo.py -- file stock.txt

beiden gebruiken stock.txt als invoer bestand
