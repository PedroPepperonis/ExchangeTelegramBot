import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

from config import API_KEY

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': 'fixer-fixer-currency-v1.p.rapidapi.com'
    }


def lst():
    data = ''
    url = 'https://fixer-fixer-currency-v1.p.rapidapi.com/latest'
    params = {'bass': 'USD'}
    response = requests.get(url, headers=headers, params=params).json()
    rates = response['rates']

    for i in rates.items():
        data += '{0}: {1} \n'.format(i[0], round(i[1], 2))

    return data


def convert(amount, from_currency, to_currency):
    url = 'https://fixer-fixer-currency-v1.p.rapidapi.com/convert'
    params = {'from': from_currency, 'to': to_currency, 'amount': amount}
    response = requests.get(url, headers=headers, params=params).json()

    query = response['query']
    from_c = query['from']
    to = query['to']
    amount = query['amount']

    result = response['result']

    data = f'From: {from_c} \n' \
           f'To: {to} \n' \
           f'Amount: {amount} \n' \
           f'Result: {result}'

    return data


def history(first, second, days):
    dates = []
    rates = []

    for i in range(int(days)):
        date = (datetime.now() - timedelta(days=i + 1)).strftime('%Y-%m-%d')
        url = f'https://fixer-fixer-currency-v1.p.rapidapi.com/{date}'
        params = {"symbols": second, "base": first}
        response = requests.request("GET", url, headers=headers, params=params).json()
        date_rate = datetime.fromisoformat(response['date']).strftime('%m.%d')
        rate = response['rates']
        for j in rate.items():
            dates.append(date_rate)
            rates.append(j[1])

    fig, ax = plt.subplots()

    dates.reverse()
    rates.reverse()
    plt.plot(dates, rates)

    diagram_path = f'images/{datetime.now().strftime("%H-%M-%S-%f")}.png'
    fig.savefig(diagram_path)

    return diagram_path
