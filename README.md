# Виджет банковских операций

## Описание проекта

Проект представляет собой виджет для обработки банковских операций клиента.

На текущем этапе реализованы функции для:

- фильтрации банковских операций по статусу;
- сортировки банковских операций по дате.

## Установка

1. Клонируйте репозиторий:

~~~bash
git clone git@github.com:Exichek/Domashka_10.1.git
~~~

2. Перейдите в директорию проекта:

~~~bash
cd Domashka_10.1
~~~

3. Установите зависимости с помощью Poetry:

~~~bash
poetry install
~~~

## Использование

Функции для обработки банковских операций находятся в модуле `src.processing`.

### Фильтрация операций по статусу

Функция `filter_by_state` принимает список словарей с банковскими операциями и возвращает новый список, содержащий только операции с указанным статусом.

По умолчанию используется статус `EXECUTED`.

Пример:

~~~python
from src.processing import filter_by_state

operations = [
    {"id": 1, "state": "EXECUTED"},
    {"id": 2, "state": "CANCELED"},
    {"id": 3, "state": "EXECUTED"},
]

result = filter_by_state(operations)
print(result)
~~~

Результат:

~~~python
[
    {"id": 1, "state": "EXECUTED"},
    {"id": 3, "state": "EXECUTED"},
]
~~~

Для фильтрации по другому статусу его можно передать вторым аргументом:

~~~python
result = filter_by_state(operations, "CANCELED")
~~~

### Сортировка операций по дате

Функция `sort_by_date` принимает список словарей с банковскими операциями и возвращает новый список, отсортированный по ключу `date`.

По умолчанию сортировка выполняется по убыванию.

Пример:

~~~python
from src.processing import sort_by_date

operations = [
    {"id": 1, "date": "2019-08-26T10:50:58.294041"},
    {"id": 2, "date": "2018-06-30T02:08:58.425572"},
    {"id": 3, "date": "2020-01-15T12:00:00.000000"},
]

result = sort_by_date(operations)
print(result)
~~~

Для сортировки по возрастанию передайте `False` вторым аргументом:

~~~python
result = sort_by_date(operations, False)
~~~

## Проверка качества кода

Для проверки проекта используются `flake8`, `mypy` и `isort`.

Запуск Flake8:

~~~bash
poetry run flake8 src
~~~

Запуск mypy:

~~~bash
poetry run mypy src
~~~

Проверка isort:

~~~bash
poetry run isort --check-only src
~~~