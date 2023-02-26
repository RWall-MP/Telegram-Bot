import requests
import json
from configs import keys


class ConvertionException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except KeyError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(
            f'https://v6.exchangerate-api.com/v6/04611af3d21ec03e2dab467b/pair/{quote_ticker}/{base_ticker}')
        total_base = json.loads(r.content)['conversion_rate']
        return total_base
