import json
from unittest.mock import mock_open, patch

from src.utils import load_transactions


def test_load_transactions():
    """Проверяет чтение списка транзакций из JSON-файла."""
    transactions = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {"code": "RUB"},
            },
        }
    ]

    with patch("builtins.open", mock_open()):
        with patch("src.utils.json.load", return_value=transactions):
            result = load_transactions("operations.json")

    assert result == transactions


def test_load_transactions_not_list():
    """Проверяет возврат пустого списка, если JSON содержит не список."""
    with patch("builtins.open", mock_open()):
        with patch("src.utils.json.load", return_value={"id": 1}):
            result = load_transactions("operations.json")

    assert result == []


def test_load_transactions_file_not_found():
    """Проверяет возврат пустого списка, если файл не найден."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_transactions("missing.json")

    assert result == []


def test_load_transactions_invalid_json():
    """Проверяет возврат пустого списка при некорректном JSON."""
    with patch("builtins.open", mock_open()):
        with patch(
            "src.utils.json.load",
            side_effect=json.JSONDecodeError("Ошибка", "", 0),
        ):
            result = load_transactions("operations.json")

    assert result == []
