import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_transaction_to_rub(transaction: dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях."""
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("API_KEY не найден")

    headers = {
        "apikey": api_key,
    }

    params = {
        "from": currency,
        "to": "RUB",
        "amount": amount,
    }

    response = requests.get(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers=headers,
        params=params,
    )

    data = response.json()

    return float(data["result"])
