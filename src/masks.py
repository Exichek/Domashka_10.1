import logging
from pathlib import Path

logs_dir = Path(__file__).resolve().parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    logs_dir / "masks.log",
    mode="w",
    encoding="utf-8",
)

file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция маскирует номер карты."""
    if not card_number:
        logger.error("Передан пустой номер карты")
        return ""

    logger.info("Номер карты успешно замаскирован")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account: str) -> str:
    """Функция скрывает номер счета."""
    if not account:
        logger.error("Передан пустой номер счета")
        return ""

    logger.info("Номер счета успешно замаскирован")
    return f"**{account[-4:]}"
