from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
import clickhouse_connect
from sqlalchemy.orm import Session
from dagster import resource

import os
from urllib.parse import quote_plus


class ChResource:
    DB_ADDRESS = os.getenv('CH_HOST', '')
    DB_PORT = os.getenv('CH_PORT', '')
    DB_USER = os.getenv('CH_USER', '')
    DB_PASSWORD = quote_plus(os.getenv('CH_PASSWORD', ''))
    DB_NAME = os.getenv('CH_DB', '')

    DB_URL = f'clickhouse://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}'

    @classmethod
    def get_client(cls):
        return clickhouse_connect.get_client(
            host=cls.DB_ADDRESS,
            port=cls.DB_PORT,
            username=cls.DB_USER,
            password=cls.DB_PASSWORD,
            database=cls.DB_NAME
        )

    @classmethod
    def get_session(cls) -> Session:
        s = Session(cls.get_engine())
        try:
            yield s
        finally:
            s.close()

    @classmethod
    def get_engine(cls) -> Engine:
        return create_engine(cls.get_uri())

    @classmethod
    def get_uri(cls) -> str:
        return cls.DB_URL

    def read(self, query, *args, **kwargs):
        return self.get_engine().execute(query).fetchall()


@resource
def ch(init_context) -> ChResource:
    return ChResource()
