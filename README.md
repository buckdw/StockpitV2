# stockpit requisites

mysql -uroot -pEmers0nFitti
create database stockpit

## general requisites
pip3 install mysql-connector-python

## stocks requisites
pip3 install lxml
pip3 install yfinance -U
pip3 install regex
pip3 install html5lib
pip3 install beautifulSoup4

https://stackoverflow.com/questions/49042224/error-in-reading-html-to-data-frame-in-python-html5lib-not-found
## stocks on Mukintosh
run /Application/Python3.8/Install.certificates for all generic certificate stuff


## execution
--drop recreates table because of DDL change
--file contains ticker symbols

python stocks.py --file stock.txt --drop

