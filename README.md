# stockpit requisites

mysql -user root --password=Emers0nFitti
create database stockpit

## general requisites
sudo pip3 install mysql-connector-python

## stocks requisites
sudo pip3 install lxml
sudo pip3 install yfinance -U
sudo pip3 install regex
sudo pip3 install html5lib

## stocks on Mukintosh
run /Application/Python3.8/Install.certificates for all generic certificate stuff


## execution
--drop recreates table because of DDL change
--file contains ticker symbols

python stocks.py --file stock.txt --drop
