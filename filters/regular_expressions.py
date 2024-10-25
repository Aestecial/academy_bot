import re
from aiogram.filters import BaseFilter
from aiogram.types import Message


class RegularExpressionsFilter(BaseFilter):
    def __init__(self, pattern: str):
        self.pattern = pattern

    async def __call__(self, message: Message) -> bool:
        text_to_check = message.text
        if text_to_check is None and message.contact:
            text_to_check = message.contact.phone_number
        return bool(re.match(self.pattern, text_to_check)) if text_to_check else False
