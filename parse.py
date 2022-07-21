import requests
from bs4 import BeautifulSoup

def get_parse():
    URL = 'https://www.nbkr.kg/XML/daily.xml'
    response = requests.get(URL)
    # print(response)
    soup = BeautifulSoup(response.text, 'xml')
    # print(soup)
    currency = soup.CurrencyRates.findAll('Currency')
    # print(currency)
    values = {'USD': currency[0].Value, 'EUR': currency[1].Value,
                'KZT': currency[2].Value, 'RUB': currency[3].Value}
    # print(values)
    return values