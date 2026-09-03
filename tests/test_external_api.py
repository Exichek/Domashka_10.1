from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_transaction_to_rub


def test_convert_transaction_rub():
    """Проверяет возврат суммы без конвертации для рублей."""
    transaction = {
        "operationAmount": {
            "amount": "31957.58",
            "currency": {"code": "RUB"},
        }
    }

    with patch("src.external_api.requests.get") as mock_get:
        result = convert_transaction_to_rub(transaction)

    assert result == 31957.58
    mock_get.assert_not_called()


def test_convert_transaction_usd():
    """Проверяет конвертацию долларов в рубли через API."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"},
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = {"result": 8730.50}

    with patch(
        "src.external_api.requests.get",
        return_value=mock_response,
    ) as mock_get:
        result = convert_transaction_to_rub(transaction)

    assert result == 8730.50
    mock_get.assert_called_once()


def test_convert_transaction_eur():
    """Проверяет конвертацию евро в рубли через API."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "EUR"},
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = {"result": 10250.75}

    with patch(
        "src.external_api.requests.get",
        return_value=mock_response,
    ) as mock_get:
        result = convert_transaction_to_rub(transaction)

    assert result == 10250.75
    mock_get.assert_called_once()


def test_convert_transaction_without_api_key():
    """Проверяет ошибку при отсутствии API-ключа."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"},
        }
    }

    with patch("src.external_api.os.getenv", return_value=None):
        with pytest.raises(ValueError, match="API_KEY не найден"):
            convert_transaction_to_rub(transaction)
