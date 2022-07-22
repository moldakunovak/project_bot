import requests
from bs4 import BeautifulSoup

def get_parse():
    URL = 'https://www.nbkr.kg/XML/daily.xml'
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'xml')
    currency = soup.CurrencyRates.findAll('Currency')
    values = {'USD': currency[0].Value, 'EUR': currency[1].Value,
                'KZT': currency[2].Value, 'RUB': currency[3].Value}
    return values