from typing import Any, cast

import pandas as pd


def read_transactions_csv(file_path: str) -> list[dict[str, Any]]:
    """Возвращает список транзакций из CSV-файла."""
    dataframe = pd.read_csv(file_path, sep=";")
    transactions = dataframe.to_dict(orient="records")

    return cast(list[dict[str, Any]], transactions)


def read_transactions_excel(file_path: str) -> list[dict[str, Any]]:
    """Возвращает список транзакций из Excel-файла."""
    dataframe = pd.read_excel(file_path)
    transactions = dataframe.to_dict(orient="records")

    return cast(list[dict[str, Any]], transactions)
