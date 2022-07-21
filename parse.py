import requests
from bs4 import BeautifulSoup
USD = 10.25

URL = 'https://www.nbkr.kg/XML/daily.xml'
response = requests.get(URL)
print(response.text)

soup = BeautifulSoup(response.text, 'lxml')
print(soup)
currency = soup.CurrencyRates.findAll('Currency')

values = {'USD': currency[0].Value, 'EUR': currency[1].Value,
          'KZT': currency[2].Value, 'RUB': currency[3].Value}
print(values)