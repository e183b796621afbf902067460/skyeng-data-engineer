from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from dagster import resource

import os
from urllib.parse import quote_plus


class DataWarehouse:
    DB_ADDRESS = os.getenv('DWH_HOST', '')
    DB_USER = os.getenv('DWH_USER', '')
    DB_PASSWORD = quote_plus(os.getenv('DWH_PASSWORD', ''))
    DB_NAME = os.getenv('DWH_DB', '')

    DB_URL = f'clickhouse://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}'

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
def dwh(init_context) -> DataWarehouse:
    return DataWarehouse()
