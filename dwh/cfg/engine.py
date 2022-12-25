from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

import os
from urllib.parse import quote_plus
from functools import lru_cache

from head.interfaces.db.settings.interface import ISettings


class DWHSettings(ISettings):
    DB_ADDRESS = os.getenv('DB_ADDRESS', 'localhost')
    DB_USER = os.getenv('DB_USER', 'default')
    DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', '111222'))
    DB_NAME = os.getenv('DB_NAME', 'clickhouse')

    DB_URL = f'clickhouse://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}'

    @classmethod
    def get_session(cls) -> Session:
        s = Session(cls.get_engine())
        try:
            yield s
        finally:
            s.close()

    @classmethod
    @lru_cache
    def get_engine(cls) -> Engine:
        return create_engine(cls.get_uri())

    @classmethod
    def get_uri(cls) -> str:
        return cls.DB_URL