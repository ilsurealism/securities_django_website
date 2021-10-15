import requests

headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'Token'
        }

# Meta Data
def get_meta_data(ticker):
    url = 'https://api.tiingo.com/tiingo/daily/{}'.format(ticker)
    response = requests.get(url, headers=headers)
    return response.json()


# Latest Price
def get_price(ticker):
    url = 'https://api.tiingo.com/tiingo/daily/{}/prices'.format(ticker)
    response = requests.get(url, headers=headers)
    if requests.get(url, headers=headers):
        return response.json()[0]


# To request daily metric data, use this endpoint
def get_daily_data(ticker):
    url = 'https://api.tiingo.com/tiingo/fundamentals/{}/daily'.format(ticker)
    response = requests.get(url, headers=headers)
    return response.json()


# To request daily metric data, use this endpoint
def get_additional_data():
    url = 'https://api.tiingo.com/tiingo/fundamentals/meta'
    response = requests.get(url, headers=headers)
    return response.json()

