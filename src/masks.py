def get_mask_card_number(card_number: str) -> str:
    """Функция маскирует номер карты"""
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account: str) -> str:
    """Функция скрывает номер счета"""
    return f"**{account[-4:]}"
