import math
from typing import Any

from src.file_readers import read_transactions_csv, read_transactions_excel
from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.utils import load_transactions
from src.widget import get_date, mask_account_card


def get_amount_and_currency(
    transaction: dict[str, Any],
) -> tuple[str, str]:
    """Возвращает сумму и валюту транзакции."""
    if "operationAmount" in transaction:
        amount = transaction["operationAmount"]["amount"]
        currency = transaction["operationAmount"]["currency"]["code"]
    else:
        amount = transaction.get("amount", "")
        currency = transaction.get("currency_code", "")

    if isinstance(amount, float) and amount.is_integer():
        amount = int(amount)

    currency_text = "руб." if currency == "RUB" else str(currency)

    return str(amount), currency_text


def get_masked_account(account: Any) -> str:
    """Возвращает замаскированные реквизиты карты или счета."""
    if account is None:
        return ""

    if isinstance(account, float) and math.isnan(account):
        return ""

    account_text = str(account)

    if not account_text:
        return ""

    return mask_account_card(account_text)


def print_transactions(
    transactions: list[dict[str, Any]],
) -> None:
    """Выводит список банковских транзакций в консоль."""
    print(
        f"\nВсего банковских операций в выборке: "
        f"{len(transactions)}\n"
    )

    for transaction in transactions:
        date = get_date(str(transaction.get("date", "")))
        description = str(transaction.get("description", ""))

        sender = get_masked_account(transaction.get("from"))
        recipient = get_masked_account(transaction.get("to"))

        amount, currency = get_amount_and_currency(transaction)

        print(f"{date} {description}")

        if sender and recipient:
            print(f"{sender} -> {recipient}")
        elif recipient:
            print(recipient)

        print(f"Сумма: {amount} {currency}")
        print()


def main() -> None:
    """Запускает программу работы с банковскими транзакциями."""
    print(
        "\nПривет! Добро пожаловать в программу работы "
        "с банковскими транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )

    transactions: list[dict[str, Any]]

    while True:
        file_choice = input("\nВведите номер пункта: ").strip()

        if file_choice == "1":
            transactions = load_transactions("data/operations.json")
            print("\nДля обработки выбран JSON-файл.")
            break

        if file_choice == "2":
            transactions = read_transactions_csv(
                "data/transactions.csv"
            )
            print("\nДля обработки выбран CSV-файл.")
            break

        if file_choice == "3":
            transactions = read_transactions_excel(
                "data/transactions_excel.xlsx"
            )
            print("\nДля обработки выбран XLSX-файл.")
            break

        print("\nТакого пункта меню нет. Попробуйте снова.")

    available_statuses = {"EXECUTED", "CANCELED", "PENDING"}

    while True:
        status = input(
            "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: "
            "EXECUTED, CANCELED, PENDING\n"
        ).strip()

        normalized_status = status.upper()

        if normalized_status in available_statuses:
            transactions = filter_by_state(
                transactions,
                normalized_status,
            )

            print(
                f'\nОперации отфильтрованы по статусу '
                f'"{normalized_status}"'
            )
            break

        print(f'\nСтатус операции "{status}" недоступен.')

    sort_choice = input(
        "\nОтсортировать операции по дате? Да/Нет\n"
    ).strip().lower()

    if sort_choice == "да":
        sort_order = input(
            "\nОтсортировать по возрастанию или по убыванию?\n"
        ).strip().lower()

        reverse = sort_order == "по убыванию"

        transactions = sort_by_date(
            transactions,
            reverse=reverse,
        )

    rub_choice = input(
        "\nВыводить только рублевые транзакции? Да/Нет\n"
    ).strip().lower()

    if rub_choice == "да":
        transactions = [
            transaction
            for transaction in transactions
            if (
                transaction.get("currency_code") == "RUB"
                or transaction.get("operationAmount", {})
                .get("currency", {})
                .get("code")
                == "RUB"
            )
        ]

    search_choice = input(
        "\nОтфильтровать список транзакций "
        "по определенному слову в описании? Да/Нет\n"
    ).strip().lower()

    if search_choice == "да":
        search = input(
            "\nВведите слово для поиска в описании:\n"
        ).strip()

        transactions = process_bank_search(
            transactions,
            search,
        )

    if not transactions:
        print(
            "\nНе найдено ни одной транзакции, "
            "подходящей под ваши условия фильтрации"
        )
        return

    print("\nРаспечатываю итоговый список транзакций...")

    print_transactions(transactions)


if __name__ == "__main__":
    main()
