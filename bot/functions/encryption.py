from typing import Optional


LETTERS = "abcdefghijklmnopqrstuvwxyz"


async def encode_telegram_id(number: int) -> Optional[str]:
    if not isinstance(number, int) or number < 0:
        return None

    encoded_str = ""

    while number > 0:
        remainder = number % 26
        number = number // 26

        if remainder == 0:
            remainder = 26
            number -= 1

        encoded_str = LETTERS[remainder - 1] + encoded_str

    return encoded_str


async def decode_telegram_id(encoded_str: str) -> Optional[int]:
    if not isinstance(encoded_str, str) or len(encoded_str) == 0:
        return None

    number = 0

    for char in encoded_str:
        if char not in LETTERS:
            return None

        number = number * 26 + (LETTERS.index(char) + 1)

    return number
