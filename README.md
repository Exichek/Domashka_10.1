# Виджет банковских операций

## Описание проекта

Проект представляет собой виджет для обработки банковских операций клиента.

На текущем этапе реализованы функции для:

- фильтрации банковских операций по статусу;
- сортировки банковских операций по дате;
- маскировки номеров банковских карт и счетов;
- преобразования даты банковской операции в формат `ДД.ММ.ГГГГ`;
- фильтрации транзакций по валюте;
- получения описаний транзакций с помощью генератора;
- генерации номеров банковских карт в заданном диапазоне.

## Установка

1. Клонируйте репозиторий:

```bash
git clone git@github.com:Exichek/Domashka_10.1.git
```

2. Перейдите в директорию проекта:

```bash
cd Domashka_10.1
```

3. Установите зависимости с помощью Poetry:

```bash
poetry install
```

## Использование

Функции для обработки банковских операций находятся в модулях `src.processing`, `src.masks`, `src.widget` и `src.generators`.

### Фильтрация операций по статусу

Функция `filter_by_state` принимает список словарей с банковскими операциями и возвращает новый список, содержащий только операции с указанным статусом.

По умолчанию используется статус `EXECUTED`.

Пример:

```python
from src.processing import filter_by_state

operations = [
    {"id": 1, "state": "EXECUTED"},
    {"id": 2, "state": "CANCELED"},
    {"id": 3, "state": "EXECUTED"},
]

result = filter_by_state(operations)
print(result)
```

Результат:

```python
[
    {"id": 1, "state": "EXECUTED"},
    {"id": 3, "state": "EXECUTED"},
]
```

Для фильтрации по другому статусу его можно передать вторым аргументом:

```python
result = filter_by_state(operations, "CANCELED")
```

### Сортировка операций по дате

Функция `sort_by_date` принимает список словарей с банковскими операциями и возвращает новый список, отсортированный по ключу `date`.

По умолчанию сортировка выполняется по убыванию.

Пример:

```python
from src.processing import sort_by_date

operations = [
    {"id": 1, "date": "2019-08-26T10:50:58.294041"},
    {"id": 2, "date": "2018-06-30T02:08:58.425572"},
    {"id": 3, "date": "2020-01-15T12:00:00.000000"},
]

result = sort_by_date(operations)
print(result)
```

Для сортировки по возрастанию передайте `False` вторым аргументом:

```python
result = sort_by_date(operations, False)
```

## Генераторы

Для работы с транзакциями с использованием генераторов и итераторов создан модуль `src.generators`.

В модуле реализованы функции:

- `filter_by_currency`;
- `transaction_descriptions`;
- `card_number_generator`.

### Фильтрация транзакций по валюте

Функция `filter_by_currency` принимает список транзакций и код валюты и возвращает итератор с транзакциями, соответствующими указанной валюте.

Пример:

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")

for transaction in usd_transactions:
    print(transaction)
```

Также значения из итератора можно получать по одному с помощью `next`:

```python
usd_transactions = filter_by_currency(transactions, "USD")

print(next(usd_transactions))
```

### Получение описаний транзакций

Функция-генератор `transaction_descriptions` принимает список транзакций и последовательно возвращает описание каждой операции.

Пример:

```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)

for description in descriptions:
    print(description)
```

Пример результата:

```text
Перевод организации
Перевод со счета на счет
Перевод с карты на карту
```

### Генерация номеров банковских карт

Функция-генератор `card_number_generator` принимает начальное и конечное значения диапазона и генерирует номера банковских карт в формате `XXXX XXXX XXXX XXXX`.

Пример:

```python
from src.generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)
```

Результат:

```text
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
0000 0000 0000 0004
0000 0000 0000 0005
```

## Тестирование

Для тестирования проекта используется библиотека `pytest`.

Тесты находятся в директории `tests` и разделены по модулям проекта:

- `test_masks.py` — тесты функций маскировки номеров карт и счетов;
- `test_widget.py` — тесты функций модуля `widget`;
- `test_processing.py` — тесты функций фильтрации и сортировки банковских операций;
- `test_generators.py` — тесты функций и генераторов модуля `generators`.

В тестах используются фикстуры `pytest` для подготовки тестовых данных и параметризация для проверки функций на различных наборах входных данных.

Для запуска всех тестов выполните:

```bash
poetry run pytest
```

Для проверки покрытия кода тестами выполните:

```bash
poetry run pytest --cov=src
```

Для создания HTML-отчета о покрытии выполните:

```bash
poetry run pytest --cov=src --cov-report=html
```

После выполнения команды HTML-отчет будет создан в директории `htmlcov`.

Открыть отчет можно через файл:

```text
htmlcov/index.html
```

Текущее покрытие функционального кода тестами составляет 100%.

## Проверка качества кода

Для проверки проекта используются `flake8`, `mypy` и `isort`.

Запуск Flake8:

```bash
poetry run flake8 src tests
```

Запуск mypy:

```bash
poetry run mypy src tests
```

Проверка isort:

```bash
poetry run isort --check-only src tests
```