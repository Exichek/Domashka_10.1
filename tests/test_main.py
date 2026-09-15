from unittest.mock import patch

import main as main_module


def test_get_amount_and_currency_json() -> None:
    """Проверяет получение суммы и валюты из JSON-транзакции."""
    transaction = {
        "operationAmount": {
            "amount": "1000.50",
            "currency": {
                "code": "RUB",
            },
        }
    }

    result = main_module.get_amount_and_currency(transaction)

    assert result == ("1000.50", "руб.")


def test_get_amount_and_currency_csv() -> None:
    """Проверяет получение суммы и валюты из CSV-транзакции."""
    transaction = {
        "amount": 1000.0,
        "currency_code": "USD",
    }

    result = main_module.get_amount_and_currency(transaction)

    assert result == ("1000", "USD")


def test_get_masked_account() -> None:
    """Проверяет маскирование реквизитов."""
    assert main_module.get_masked_account(None) == ""
    assert main_module.get_masked_account(float("nan")) == ""
    assert main_module.get_masked_account("") == ""

    assert (
        main_module.get_masked_account(
            "Счет 12345678901234567890"
        )
        == "Счет **7890"
    )


def test_print_transactions(capsys) -> None:
    """Проверяет вывод транзакций в консоль."""
    transactions = [
        {
            "date": "2023-09-05T11:30:32Z",
            "description": "Перевод организации",
            "amount": 1000.0,
            "currency_code": "RUB",
            "from": "Счет 12345678901234567890",
            "to": "Счет 98765432109876543210",
        },
        {
            "date": "2023-09-06T11:30:32Z",
            "description": "Открытие вклада",
            "amount": 500.0,
            "currency_code": "USD",
            "from": None,
            "to": "Счет 11112222333344445555",
        },
    ]

    main_module.print_transactions(transactions)

    captured = capsys.readouterr()

    assert "Всего банковских операций в выборке: 2" in captured.out
    assert "05.09.2023 Перевод организации" in captured.out
    assert "Счет **7890 -> Счет **3210" in captured.out
    assert "Сумма: 1000 руб." in captured.out

    assert "06.09.2023 Открытие вклада" in captured.out
    assert "Счет **5555" in captured.out
    assert "Сумма: 500 USD" in captured.out


def test_main_csv_full_flow() -> None:
    """Проверяет полный сценарий работы с CSV."""
    transactions = [
        {
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "description": "Перевод организации",
            "amount": 1000.0,
            "currency_code": "RUB",
            "from": "Счет 12345678901234567890",
            "to": "Счет 98765432109876543210",
        }
    ]

    user_input = [
        "2",
        "executed",
        "да",
        "по убыванию",
        "да",
        "да",
        "перевод",
    ]

    with (
        patch(
            "builtins.input",
            side_effect=user_input,
        ),
        patch(
            "main.read_transactions_csv",
            return_value=transactions,
        ) as mock_csv,
        patch(
            "main.filter_by_state",
            return_value=transactions,
        ) as mock_filter,
        patch(
            "main.sort_by_date",
            return_value=transactions,
        ) as mock_sort,
        patch(
            "main.process_bank_search",
            return_value=transactions,
        ) as mock_search,
        patch(
            "main.print_transactions"
        ) as mock_print,
    ):
        main_module.main()

    mock_csv.assert_called_once_with(
        "data/transactions.csv"
    )

    mock_filter.assert_called_once_with(
        transactions,
        "EXECUTED",
    )

    mock_sort.assert_called_once_with(
        transactions,
        reverse=True,
    )

    mock_search.assert_called_once_with(
        transactions,
        "перевод",
    )

    mock_print.assert_called_once_with(transactions)


def test_main_json_invalid_input(capsys) -> None:
    """Проверяет неверный пункт меню, статус и пустую выборку."""
    user_input = [
        "10",
        "1",
        "test",
        "executed",
        "нет",
        "нет",
        "нет",
    ]

    with (
        patch(
            "builtins.input",
            side_effect=user_input,
        ),
        patch(
            "main.load_transactions",
            return_value=[],
        ) as mock_json,
        patch(
            "main.filter_by_state",
            return_value=[],
        ),
        patch(
            "main.print_transactions"
        ) as mock_print,
    ):
        main_module.main()

    captured = capsys.readouterr()

    assert "Такого пункта меню нет" in captured.out
    assert 'Статус операции "test" недоступен' in captured.out
    assert "Не найдено ни одной транзакции" in captured.out

    mock_json.assert_called_once_with(
        "data/operations.json"
    )

    mock_print.assert_not_called()


def test_main_excel_flow() -> None:
    """Проверяет сценарий работы с XLSX."""
    transactions = [
        {
            "state": "PENDING",
            "date": "2023-09-05T11:30:32Z",
            "description": "Открытие вклада",
            "amount": 500.0,
            "currency_code": "USD",
            "from": None,
            "to": "Счет 11112222333344445555",
        }
    ]

    user_input = [
        "3",
        "pending",
        "нет",
        "нет",
        "нет",
    ]

    with (
        patch(
            "builtins.input",
            side_effect=user_input,
        ),
        patch(
            "main.read_transactions_excel",
            return_value=transactions,
        ) as mock_excel,
        patch(
            "main.filter_by_state",
            return_value=transactions,
        ),
        patch(
            "main.print_transactions"
        ) as mock_print,
    ):
        main_module.main()

    mock_excel.assert_called_once_with(
        "data/transactions_excel.xlsx"
    )

    mock_print.assert_called_once_with(transactions)
