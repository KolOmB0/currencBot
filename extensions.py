import json
import requests
from config import exchanges

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        # Парсим валюты
        url = f"https://api.apilayer.com/currency_data/convert?to={sym_key}&from={base_key}&amount={amount}"
        payload = {}
        headers = {
            "apikey": "khPHdKv4o1a5NQAavrwZPvXVcnP0LLGm"
        }

        r = requests.request("GET", url, headers=headers, data=payload)
        # Ключи валют  base - из которой переводим  rates/result в какую перерводим
        # amount - количесто волюты
        resp = json.loads(r.content)

        new_price = resp['result']
        new_price = round(new_price, 3)
        message =  f"Цена {amount} {base} в {sym} : {new_price}"
        return message
