import json
import logging
from pathlib import Path
from typing import Any

logs_dir = Path(__file__).resolve().parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    logs_dir / "utils.log",
    mode="w",
    encoding="utf-8",
)

file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> list[dict[str, Any]]:
    """Возвращает список финансовых транзакций из JSON-файла."""
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            logger.info("Транзакции успешно загружены из файла %s", file_path)
            return data

        logger.error("JSON-файл %s содержит данные не в виде списка", file_path)
        return []

    except FileNotFoundError:
        logger.error("Файл %s не найден", file_path)
        return []

    except json.JSONDecodeError:
        logger.error("Ошибка чтения JSON-файла %s", file_path)
        return []
