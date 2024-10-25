import os
from dataclasses import dataclass
from typing import List
from environs import Env

env = Env()
env.read_env()

@dataclass
class TgBot:
    token: str
    admin_ids: List[int]


@dataclass
class Config:
    tg_bot: TgBot


def load_config() -> Config:
    admin_ids_str = os.getenv("ADMIN_IDS", "")
    admin_ids_list = [int(id_str) for id_str in admin_ids_str.split(",") if id_str]
    return Config(
        tg_bot=TgBot(
            token=os.getenv("BOT_TOKEN"),
            admin_ids=admin_ids_list
        )
    )
