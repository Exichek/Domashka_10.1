from unittest.mock import Mock, patch

from src.file_readers import read_transactions_csv, read_transactions_excel


def test_read_transactions_csv() -> None:
    """Проверяет чтение транзакций из CSV-файла."""
    mock_dataframe = Mock()
    mock_dataframe.to_dict.return_value = [
        {
            "id": 1,
            "state": "EXECUTED",
            "amount": 1000,
        }
    ]

    with patch(
        "src.file_readers.pd.read_csv",
        return_value=mock_dataframe,
    ) as mock_read_csv:
        result = read_transactions_csv("test.csv")

    mock_read_csv.assert_called_once_with("test.csv", sep=";")
    mock_dataframe.to_dict.assert_called_once_with(orient="records")

    assert result == [
        {
            "id": 1,
            "state": "EXECUTED",
            "amount": 1000,
        }
    ]


def test_read_transactions_excel() -> None:
    """Проверяет чтение транзакций из Excel-файла."""
    mock_dataframe = Mock()
    mock_dataframe.to_dict.return_value = [
        {
            "id": 2,
            "state": "CANCELED",
            "amount": 500,
        }
    ]

    with patch(
        "src.file_readers.pd.read_excel",
        return_value=mock_dataframe,
    ) as mock_read_excel:
        result = read_transactions_excel("test.xlsx")

    mock_read_excel.assert_called_once_with("test.xlsx")
    mock_dataframe.to_dict.assert_called_once_with(orient="records")

    assert result == [
        {
            "id": 2,
            "state": "CANCELED",
            "amount": 500,
        }
    ]
